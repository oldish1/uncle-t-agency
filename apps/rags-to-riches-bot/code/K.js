// Does this message ask to change or cancel an existing booking?
const t = String(input.text || "").toLowerCase();
const yes = t.length > 0 && t.length < 300 &&
  /\b(cancel|cancell?ation|change|reschedul|re-schedul|postpone|move (my|the|our) (booking|clean)|kanselleer|verander|skuif)/.test(t);
return { is_manage: yes ? "yes" : "no" };
