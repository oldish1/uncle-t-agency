"""Run: python -m unittest discover apps/lead-finder/tests"""

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import outreach  # noqa: E402
import site_check  # noqa: E402
import sources  # noqa: E402
from scoring import Review, Salon, score  # noqa: E402

RECENT = (datetime.now(timezone.utc) - timedelta(days=20)).isoformat()


def salon(**kw):
    base = dict(place_id="p1", name="Glow Hair Studio", phone="072 123 4567", rating=4.6, review_count=85)
    base.update(kw)
    return Salon(**base)


class Scoring(unittest.TestCase):
    def test_pain_heavy_salon_with_no_website_is_hot(self):
        s = salon(reviews=[
            Review("Great braids but they never replied to my WhatsApp for 3 days", 3, RECENT),
            Review("Lovely lady. They double booked me and I had to come back another day", 2, RECENT),
            Review("Best colour in Bellville!", 5, RECENT, owner_reply="So sorry we missed your message, we were swamped"),
        ])
        sc = score(s)
        self.assertEqual(sc.tier, "Hot")
        self.assertEqual(sc.pitch, "Lexi + website")
        self.assertIn("missed_messages", sc.pain_types)
        self.assertIn("double_booking", sc.pain_types)
        self.assertTrue(any("never replied" in e for e in sc.evidence))

    def test_happy_salon_scores_low_on_need(self):
        sc = score(salon(website="https://glow.co.za", site={"booking_tool": ""},
                         reviews=[Review("Amazing service, will be back", 5, RECENT)]))
        self.assertLess(sc.need, 15)
        self.assertEqual(sc.website, 0)

    def test_fresha_user_is_not_pitched_lexi(self):
        s = salon(website="https://glow.co.za", site={"booking_tool": "Fresha"},
                  reviews=[Review("They didn't reply to my message", 3, RECENT)])
        sc = score(s)
        self.assertEqual(sc.booking_tool, "Fresha")
        self.assertNotIn("Lexi", sc.pitch)

    def test_chain_and_closed_are_skipped(self):
        self.assertEqual(score(salon(name="Sorbet Tyger Valley")).tier, "Skip")
        self.assertEqual(score(salon(status="CLOSED_PERMANENTLY")).tier, "Skip")

    def test_facebook_page_counts_as_no_real_website(self):
        sc = score(salon(website="https://www.facebook.com/glowhair"))
        self.assertEqual(sc.website, 12)

    def test_afrikaans_complaint_is_caught(self):
        sc = score(salon(reviews=[Review("Hulle antwoord nie op WhatsApp nie", 2, RECENT)]))
        self.assertIn("missed_messages", sc.pain_types)

    def test_tiny_salon_scores_low_on_can_pay(self):
        sc = score(salon(review_count=3, rating=5.0))
        self.assertLess(sc.can_pay, 15)


class Sources(unittest.TestCase):
    def test_places_response_is_read(self):
        page = {"places": [{
            "id": "abc", "displayName": {"text": "Braids by Naeema"}, "formattedAddress": "12 Voortrekker Rd, Parow",
            "nationalPhoneNumber": "082 555 0101", "rating": 4.4, "userRatingCount": 57,
            "businessStatus": "OPERATIONAL", "googleMapsUri": "https://maps.google.com/?cid=1",
            "reviews": [{"rating": 2, "publishTime": RECENT, "text": {"text": "No reply on WhatsApp"}}],
        }]}
        resp = mock.Mock(status_code=200, ok=True, json=lambda: page)
        with mock.patch.object(sources, "get_env", return_value="k"), \
             mock.patch.object(sources.requests, "post", return_value=resp) as post:
            out = sources.google_search("braiding salon", "Parow")
        self.assertEqual(post.call_args.kwargs["json"]["textQuery"], "braiding salon in Parow, Cape Town")
        self.assertEqual(out[0].name, "Braids by Naeema")
        self.assertEqual(out[0].reviews[0].text, "No reply on WhatsApp")

    def test_bad_key_gives_plain_message(self):
        resp = mock.Mock(status_code=403, ok=False, text="PERMISSION_DENIED")
        with mock.patch.object(sources, "get_env", return_value="k"), \
             mock.patch.object(sources.requests, "post", return_value=resp):
            with self.assertRaises(sources.SourceError) as e:
                sources.google_search("hair salon", "Bellville")
        self.assertIn("Places API", str(e.exception))

    def test_apify_item_is_read(self):
        s = sources.from_apify_json({
            "title": "Nails by Zee", "placeId": "z1", "phone": "+27 61 222 3333", "totalScore": 4.8,
            "reviewsCount": 140, "permanentlyClosed": False,
            "reviews": [{"text": "Took forever to reply", "stars": 3, "publishedAtDate": RECENT,
                         "responseFromOwnerText": "Apologies for the delay!"}],
        }, "Kuils River")
        sc = score(s)
        self.assertIn("missed_messages", sc.pain_types)
        self.assertTrue(any("apologised" in r for r in sc.reasons))


class SiteAndMessage(unittest.TestCase):
    def test_booking_tool_and_whatsapp_detected(self):
        info = site_check.read_html('<a href="https://www.fresha.com/a/glow">Book</a> <a href="https://wa.me/27721234567">')
        self.assertEqual(info["booking_tool"], "Fresha")
        self.assertTrue(info["whatsapp_booking"])

    def test_blocked_network_is_neutral(self):
        with mock.patch.object(site_check.requests, "get", side_effect=site_check.requests.exceptions.ProxyError()):
            info = site_check.check("https://glow.co.za")
        self.assertEqual(info, {"unchecked": True})
        sc = score(salon(website="https://glow.co.za", site=info))
        self.assertEqual(sc.website, 0)

    def test_message_leads_with_pain_and_never_says_ai(self):
        s = salon(reviews=[Review("never replied to my whatsapp", 2, RECENT)])
        msg = outreach.first_message(s, score(s))
        self.assertIn("struggling to get a reply", msg)
        self.assertNotRegex(msg.lower(), r"\bai\b|chatbot|—")

    def test_whatsapp_link(self):
        self.assertEqual(outreach.whatsapp_link("072 123 4567"), "https://wa.me/27721234567")
        self.assertEqual(outreach.whatsapp_link("021 555"), "")


class EndToEnd(unittest.TestCase):
    def test_rescore_from_raw_writes_report_and_csv(self):
        salons = [
            salon(place_id="a", name="Glow Hair Studio", reviews=[Review("never replied, double booked me", 2, RECENT)]),
            salon(place_id="b", name="Sorbet Canal Walk"),
            salon(place_id="c", name="CHALES Hair Boutique"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "raw.json"
            raw.write_text(json.dumps([asdict(s) for s in salons]))
            out = Path(tmp) / "out"
            subprocess.run([sys.executable, str(HERE.parent / "lead_finder.py"), "--from-raw", str(raw),
                            "--out", str(out)], check=True, capture_output=True)
            report = (out / "report.md").read_text()
            csv_text = (out / "leads.csv").read_text()
        self.assertIn("Glow Hair Studio", report)
        self.assertNotIn("## 2.", report)          # chain and pipeline salon aren't written up
        self.assertIn("already in the pipeline", csv_text)
        self.assertIn("chain or franchise", csv_text)


if __name__ == "__main__":
    unittest.main()
