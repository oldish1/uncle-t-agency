/* Flat drawings of the shop's work, in one graphic language. Replace with the shop's own photos when available. */
const ST = '#9aa3ab', DK = '#15191d', MD = '#6b757e', LT = '#c9ced3', OR = '#e2460f', CU = '#b8673a', CU2 = '#8f4a24', CU3 = '#a35a30';

const ART = {
  laser: ({ bg }) => (
    <svg viewBox="0 0 240 300" role="img" aria-label="Drawing of a flat part being laser cut from a steel plate">
      <rect width="240" height="300" fill={bg} />
      <rect x="20" y="30" width="200" height="240" fill={ST} />
      <rect x="48" y="66" width="144" height="168" rx="14" fill="#b9c1c8" stroke={DK} strokeWidth="4" />
      {[[76, 96], [164, 96], [76, 204], [164, 204]].map(([x, y]) => <circle key={x + y} cx={x} cy={y} r="10" fill={DK} />)}
      <rect x="100" y="142" width="40" height="16" rx="8" fill={DK} />
      <rect x="0" y="140" width="240" height="20" fill={DK} opacity=".9" />
      <rect x="170" y="128" width="46" height="44" fill="#46515b" />
      <circle cx="192" cy="150" r="20" fill={OR} opacity=".3" />
      <circle cx="192" cy="150" r="7" fill={OR} />
      <circle cx="192" cy="150" r="3" fill="#fff" />
    </svg>
  ),
  brake: ({ bg }) => (
    <svg viewBox="0 0 320 213" role="img" aria-label="Drawing of a press brake punch folding a steel sheet into a die">
      <rect width="320" height="213" fill={bg} />
      <rect x="0" y="0" width="22" height="213" fill="#10151a" /><rect x="298" y="0" width="22" height="213" fill="#10151a" />
      <path d="M22 213 V150 H130 L160 180 L190 150 H298 V213 Z" fill="#323d46" />
      <rect x="22" y="205" width="276" height="8" fill={OR} />
      <path d="M92 150 L160 84 L228 150" fill="none" stroke={LT} strokeWidth="12" strokeLinejoin="round" />
      <rect x="22" y="0" width="276" height="22" fill="#2c353d" />
      <path d="M136 22 H184 V40 L160 86 L136 40 Z" fill={MD} />
      <path d="M150 66 L160 86 L170 66 Z" fill={OR} />
    </svg>
  ),
  punch: ({ bg }) => (
    <svg viewBox="0 0 200 200" role="img" aria-label="Drawing of a steel sheet with punched round, square and slot holes">
      <rect width="200" height="200" fill={bg} />
      <rect x="16" y="24" width="168" height="152" fill={ST} />
      <g fill={DK}>
        {[44, 84, 124].map(x => <circle key={'c' + x} cx={x} cy="52" r="9" />)}
        {[35, 75, 115].map(x => <rect key={'s' + x} x={x} y="87" width="18" height="18" />)}
        {[33, 73, 113].map(x => <rect key={'l' + x} x={x} y="132" width="24" height="12" rx="6" />)}
      </g>
      <circle cx="160" cy="52" r="9" fill={OR} />
    </svg>
  ),
  still: ({ bg }) => (
    <svg viewBox="0 0 240 300" role="img" aria-label="Drawing of a copper pot still with a swan neck and condenser">
      <rect width="240" height="300" fill={bg} />
      <rect x="30" y="262" width="180" height="14" fill={DK} />
      <ellipse cx="100" cy="206" rx="64" ry="54" fill={CU} />
      <path d="M72 164 Q68 120 100 104 Q132 120 128 164 Z" fill={CU3} />
      <ellipse cx="100" cy="80" rx="20" ry="28" fill={CU} />
      <path d="M114 62 Q160 40 188 70 L188 110" fill="none" stroke={CU} strokeWidth="13" strokeLinecap="round" />
      <rect x="170" y="108" width="36" height="140" fill={CU2} />
      <rect x="166" y="104" width="44" height="10" fill={DK} />
      <circle cx="100" cy="208" r="10" fill={OR} />
    </svg>
  ),
  mincer: ({ bg }) => (
    <svg viewBox="0 0 320 213" role="img" aria-label="Drawing of a Supra meat mincer with hopper and tray">
      <rect width="320" height="213" fill={bg} />
      <rect x="50" y="176" width="220" height="14" fill={DK} />
      <rect x="86" y="108" width="148" height="68" fill={ST} />
      <path d="M96 108 L124 40 H196 L224 108 Z" fill={LT} />
      <rect x="234" y="124" width="38" height="36" fill={MD} />
      <rect x="270" y="120" width="8" height="44" fill="#3b454f" />
      <rect x="40" y="150" width="46" height="8" fill={MD} />
      <circle cx="120" cy="142" r="11" fill={OR} />
    </svg>
  ),
  /* the small drop-cap version of the still */
  dropstill: ({ bg }) => (
    <svg viewBox="0 0 120 120" role="img" aria-label="Drawing of a copper pot still">
      <rect width="120" height="120" fill={bg} />
      <rect x="18" y="102" width="84" height="8" fill={DK} />
      <ellipse cx="52" cy="78" rx="30" ry="25" fill={CU} />
      <path d="M38 58 Q36 38 52 32 Q68 38 66 58 Z" fill={CU3} />
      <ellipse cx="52" cy="24" rx="9" ry="12" fill={CU} />
      <path d="M58 16 Q78 8 92 22 L92 36" fill="none" stroke={CU} strokeWidth="6" strokeLinecap="round" />
      <rect x="84" y="36" width="16" height="50" fill={CU2} /><rect x="82" y="34" width="20" height="5" fill={DK} />
      <circle cx="52" cy="80" r="5" fill={OR} />
    </svg>
  )
};

export function Art({ name, bg = '#dcdfe1' }) {
  const C = ART[name === 'still' && bg === '#dcdfe1' ? 'dropstill' : name];
  return C({ bg });
}
