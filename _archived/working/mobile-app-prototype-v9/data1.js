// Part 1 of guidebook v9

export const POPS = [
  { code:"MOB", label:"Mobility & Strength", desc:"Wheelchair users, ambulant mobility, reduced strength and endurance." },
  { code:"VIS", label:"Vision Impairment", desc:"Blind, low vision, colour vision deficiency. Tactile and auditory environment critical." },
  { code:"DEAF", label:"Deaf / Hard of Hearing", desc:"Deaf, hard of hearing, hearing device users. Visual environment and STI critical." },
  { code:"NEU", label:"Neurological / ABI", desc:"Acquired brain injury, post-concussion syndrome, stroke. Sensory sensitivity and fatigue." },
  { code:"DEM", label:"Dementia", desc:"All dementia types. Wayfinding, cognitive simplicity, familiar environments." },
  { code:"NDV", label:"Neurodivergence", desc:"Autism, ADHD, sensory processing differences. Sensory control paramount." },
  { code:"NDV/MH", label:"Mental Health & PTSD", desc:"PTSD, trauma-informed design, anxiety, depression. Defensible space and autonomy." },
  { code:"PAIN", label:"Chronic Pain", desc:"Chronic pain conditions, fibromyalgia. Vibration control, warmth, rest." },
  { code:"DBL", label:"DeafBlind", desc:"Combined deaf and blind, distinct from VIS or DEAF alone. Tactile communication paramount." },
  { code:"OFS", label:"Orthostatic & Fatigue", desc:"ME/CFS, POTS, MCAS. Positional tolerance, rest, environmental sensitivity." },
];

export const CATEGORIES = [
  { letter:"A", name:"Acoustics" },
  { letter:"B", name:"Lighting" },
  { letter:"C", name:"Colour & Surface" },
  { letter:"D", name:"Spatial & Wayfinding" },
  { letter:"E", name:"Entry & Circulation" },
  { letter:"F", name:"Sensory Zoning" },
  { letter:"G", name:"Furniture & Fixtures" },
  { letter:"H", name:"Controls & Technology" },
  { letter:"I", name:"Upper Limb" },
];

export const TIERS = [
  { v:0, n:"Universal", d:"Code compliance. The floor — not the aspiration." },
  { v:1, n:"Population-Informed", d:"Evidence-based ranges. The aspiration of this guidebook." },
  { v:2, n:"Person-Specific", d:"OT assessment resolves position within the range." },
];

export const TOPICS = [
  { id:"sensory", label:"Sensory environment" },
  { id:"lighting", label:"Lighting" },
  { id:"wayfinding", label:"Wayfinding" },
  { id:"refuge", label:"Refuge" },
  { id:"control", label:"Personal control" },
  { id:"entry", label:"Entry" },
  { id:"circulation", label:"Circulation" },
  { id:"materials", label:"Materials" },
  { id:"safety", label:"Safety" },
  { id:"toileting", label:"Toileting" },
  { id:"communication", label:"Communication" },
];
