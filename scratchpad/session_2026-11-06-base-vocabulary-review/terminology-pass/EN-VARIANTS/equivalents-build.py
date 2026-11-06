"""Regenerate equivalents.tsv for EN-VARIANTS and exit 1 if any quote is not verbatim
(whitespace-collapsed) in the saved text of its source, or exceeds 25 words.
Run: python3 -I <this file>. Texts are under text/ (not committed; fetch again by the
manifest URL and sha256 in retrieval-log/session_2026-11-06-base-vocabulary-review/)."""
import csv, os, re, sys
D = os.path.dirname(os.path.abspath(__file__)); SES = os.path.dirname(os.path.dirname(D))
# source key -> (title as written, issuer, jurisdiction, url, text file)
S = {
 'US': ('2010 ADA Standards for Accessible Design', 'U.S. Department of Justice', 'US', 'https://www.ada.gov/law-and-regs/design-standards/2010-stds/', 'text/a2f0dc7adef4.txt'),
 'UK': ('Approved Document M Volume 2, 2015 edition incorporating 2020 and 2024 amendments (For use in England)', 'UK Government (England)', 'UK-ENG', 'https://assets.publishing.service.gov.uk/media/66f6c5eec71e42688b65ee11/ADM__V2_with_2024_amendments.pdf', 'text/0e5d4dee25b3.txt'),
 'SG': ('Code on Accessibility in the Built Environment 2025 (Version 1.1)', 'Building and Construction Authority', 'SG', 'https://file.go.gov.sg/bca-coa2025.pdf', 'text/846c3044c174.txt'),
 'AU': ('Disability (Access to Premises — Buildings) Standards 2010, Compilation No. 3 (Schedule 1 Access Code)', 'Commonwealth of Australia', 'AU', 'https://www.legislation.gov.au/F2010L00668/2024-11-23/2024-11-23/text/original/pdf', 'text/7aab78bfba5f.txt'),
 'NZ': ('Acceptable Solutions and Verification Methods for New Zealand Building Code Clause D1 Access Routes (2nd ed. amd 6)', 'Ministry of Business, Innovation and Employment', 'NZ', 'https://web.archive.org/web/20261022090808if_/https://www.building.govt.nz/assets/Uploads/building-code-compliance/d-access/d1-access-routes/asvm/d1-access-routes-2nd-edition-amendment6.pdf', 'text/02132b6af9ba.txt'),
 'IE': ('Building Regulations Technical Guidance Document M 2022 Access and Use', 'Department of Housing, Local Government and Heritage (council-hosted copy)', 'IE', 'https://www.galway.ie/sites/default/files/2025-07/Technical%20Guidance%20Document%20Part%20M%20-%20Access%20and%20Use%202022.pdf', 'text/e6042db0542a.txt'),
 'B651': ('CSA/ASC B651:23 Accessible design for the built environment (clause headings)', 'CSA Group / Accessibility Standards Canada', 'CA', 'see register b651-headings.tsv', '../../b651-headings.tsv'),
 'RHFAC': ('RHFAC Rating Survey v4.0', 'Rick Hansen Foundation', 'CA', 'see register rhfac-criteria.tsv', '../../rhfac-criteria.tsv'),
 'NY': ('New York Vehicle and Traffic Law, § 1203-B Parking spaces; handicapped', 'New York State Senate (Open Legislation)', 'US-NY', 'https://www.nysenate.gov/legislation/laws/VAT/1203-B', 'text/eq-6091a31d4d5c.txt'),
 'UKBADGE': ('The Disabled Persons (Badges for Motor Vehicles) (England) Regulations 2000 (SI 2000/682), as made', 'UK Government', 'UK-ENG', 'https://www.legislation.gov.uk/uksi/2000/682/made', 'text/eq-ea6351aae5e4.txt'),
 'IESI': ('Road Traffic (Traffic and Parking) Regulations, 1997 (S.I. No. 182/1997)', 'Government of Ireland (Irish Statute Book)', 'IE', 'https://www.irishstatutebook.ie/eli/1997/si/182/made/en/print', 'text/eq-f92c0d227868.txt'),
 'WA': ('Local Government (Parking for People with Disabilities) Regulations 2014', 'Western Australia', 'AU-WA', 'https://www.legislation.wa.gov.au/legislation/prod/filestore.nsf/FileURL/mrdoc_42731.htm/$FILE/Local%20Government%20(Parking%20for%20People%20with%20Disabilities)%20Regulations%202014%20-%20%5B00-c0-00%5D.html', 'text/eq-1a252efe5202.txt'),
 'ON581': ('R.R.O. 1990, Reg. 581: Accessible Parking for Persons with Disabilities (Highway Traffic Act)', 'Ontario e-Laws', 'CA-ON', 'https://www.ontario.ca/laws/regulation/900581', 'text/eq-5f9b8b544c8f.txt'),
 'ON209': ('O. Reg. 209/01: Elevating Devices (Technical Standards and Safety Act, 2000)', 'Ontario e-Laws', 'CA-ON', 'https://www.ontario.ca/laws/regulation/010209', 'text/eq-b2acf7df9b4f.txt'),
 'ACA': ('Accessible Canada Act (S.C. 2019, c. 10)', 'Justice Laws Website, Government of Canada', 'CA', 'https://laws-lois.justice.gc.ca/eng/acts/A-0.6/FullText.html', 'text/eq-38e031a479bb.txt'),
 'TOR': ('City of Toronto Zoning By-law 569-2013, Chapter 200.15 (new provision)', 'City of Toronto', 'CA-ON', 'https://www.toronto.ca/zoning/bylaw%5Famendments/ZBL_NewProvision_Chapter200_15.htm', 'text/eq-34259fb864c2.txt'),
 'MUTCD': ('Manual on Uniform Traffic Control Devices, 2009 Edition, Part 2B (superseded by the 11th edition)', 'Federal Highway Administration', 'US', 'https://mutcd.fhwa.dot.gov/htm/2009/part2/part2b.htm', 'text/eq-a8f3e3a8ff09.txt'),
 'KYTS': ('Know your traffic signs: on-street parking control signs and road markings', 'Department for Transport', 'UK', 'https://www.gov.uk/government/publications/know-your-traffic-signs/on-street-parking-control-signs-and-road-markings', 'text/eq-91e6b01f121a.txt'),
 'NI': ('Disabled Badge Holders Only At All Times Sign', 'Department for Infrastructure (Northern Ireland)', 'UK-NIR', 'https://www.infrastructure-ni.gov.uk/publications/disabled-badge-holders-only-all-times-sign', 'text/eq-7022a5b345d8.txt'),
 'GOVBB': ('Apply for or renew a Blue Badge', 'GOV.UK', 'UK', 'https://www.gov.uk/apply-blue-badge', 'text/eq-0f0826b58ed2.txt'),
 'USAB': ('Guide to the ADA Accessibility Standards, Chapter 5: Parking', 'U.S. Access Board', 'US', 'https://www.access-board.gov/ada/guides/chapter-5-parking/', 'text/eq-68cdbb4e2cba.txt'),
 'CADMV': ('Disabled Person Parking Placards & Plates', 'California DMV', 'US-CA', 'https://www.dmv.ca.gov/portal/vehicle-registration/disabled-person-parking-placards-plates/', 'text/eq-70930685b8c5.txt'),
 'ADANN': ('Guidelines for Writing About People With Disabilities', 'ADA National Network', 'US', 'https://adata.org/factsheet/ADANN-writing', 'text/eq-50a9025a245a.txt'),
 'NORTH': ('Language and disability (council guidance citing the Office for Disability Issues)', 'Northumberland County Council', 'UK-ENG', 'https://www.northumberland.gov.uk/NorthumberlandCountyCouncil/media/About-the-Council/equality/Language-Disability.pdf', 'text/eq-93a4dca2e6a6.txt'),
 'DARWIN': ('Disability Parking Permits', 'City of Darwin', 'AU-NT', 'https://www.darwin.nt.gov.au/sites/default/files/page/file/Disability%20Parking%20Permits.pdf', 'text/eq-fc24ec8b34a0.txt'),
 'BELL': ('Accessible Services, Information and Features', 'Bellingen Shire Council', 'AU-NSW', 'https://www.bellingen.nsw.gov.au/Community/Community-Support/People-with-Disability/Accessible-Services-Information-and-Features', 'text/eq-32a36a2ae646.txt'),
 'DAREBIN': ('Accessible facilities', 'Darebin Libraries (Darebin City Council)', 'AU-VIC', 'https://libraries.darebin.vic.gov.au/services/accessibility/accessible-facilities', 'text/eq-68abbbf5f380.txt'),
 'GLEN': ('Disability access and getting around', 'Glen Eira City Council', 'AU-VIC', 'https://www.gleneira.vic.gov.au/services/disability-and-accessibility/disability-access-and-getting-around', 'text/eq-86e1882bd639.txt'),
 'SGEG': ('Car Park Label Scheme (Enabling Guide)', 'SG Enable', 'SG', 'https://www.enablingguide.sg/im-looking-for-disability-support/transport/car-park-label-scheme', 'text/eq-f087e6f007f5.txt'),
 'MSF': ('Number of applications received for HDB season parking for disabled car park lots (parliamentary reply)', 'Ministry of Social and Family Development', 'SG', 'https://msf.gov.sg/media-room/article/Number-of-applications-received-for-HDB-season-parking-for-disabled-car-park-lots', 'text/eq-1b4445080240.txt'),
 'ONAPP': ('Get an accessible parking permit', 'Government of Ontario (ServiceOntario)', 'CA-ON', 'https://www.ontario.ca/page/get-accessible-parking-permit', 'text/eq-1afbf8bfed40.txt'),
 'SSM': ('Zoning By-law parking amendments package', 'City of Sault Ste. Marie', 'CA-ON', 'https://saultstemarie.ca/wp-content/uploads/2025/10/Zoning_ParkingAmendments_PKG.pdf', 'text/eq-5a26f5582fae.txt'),
 'UOA': ('Accessible spaces and car parking', 'University of Auckland', 'NZ', 'https://www.auckland.ac.nz/en/about-us/about-the-university/equity-diversity-inclusion/facilities-spaces/accessible-spaces-parking.html', 'text/eq-9fe9bbe69d88.txt'),
 'CCS': ('Mobility Parking Support', 'CCS Disability Action', 'NZ', 'https://www.ccsdisabilityaction.org.nz/mobility-parking', 'text/eq-3d6e27e8be13.txt'),
}
L = {'R2-050': 'designated accessible spaces', 'R2-053': 'Access aisle', 'R2-052': 'Passenger pick-up areas', 'R2-059': 'Curb ramps',
     'R2-072': 'Accessible route', 'R2-074': 'Accessible path of travel', 'R2-156': 'Vision panels', 'R2-163': 'Elevators', 'R2-164': 'Elevating devices',
     'R2-168': 'Platform lifts', 'R2-169': 'stair lift', 'R2-177': 'Universal washrooms', 'R2-208': 'Pictogram of accessibility',
     'R2-281': 'Parking', 'R2-333': 'Accessible'}
PARK_PERMIT = 'names the permit or its holder, used to name the space ("badge holders only"); NARROWER than the space concept as a form, kept because people search with it'
HANDI = 'Usage note: disfavoured by many disabled people and listed as outdated in US and UK language guidance, still in force in statute and signs'
# (concept, form, usage_type, scope_note, tier, source, locator, quote, conflation)
R = [
 # ---------- parking: tier 1 ----------
 ('R2-050','Accessible Parking Spaces','code term','','1','US','208.2, Table 208.2 (text L772)','Minimum Number of Required Accessible Parking Spaces',''),
 ('R2-050','Van Parking Spaces','code term','NARROWER: a subclass of the accessible space','1','US','208.2.4 (text L808)','208.2.4 Van Parking Spaces.',''),
 ('R2-050','parking bay designated for disabled people','code term','','1','UK','1.18 a, PDF p20 L1952','at least one parking bay designated for disabled people is provided on firm and level ground',''),
 ('R2-050','designated parking bays','code term','short form of the same bay in the same clause','1','UK','1.18 b, PDF p20 L1956','the dimensions of the designated parking bays are as shown in Diagram 2',''),
 ('R2-050','accessible parking lot','code term','','1','SG','3.3.1 Functional Intent, PDF p26 L2002','The accessible parking lot must be clearly marked, easy to locate and access.',''),
 ('R2-050','Designated accessible vehicle parking lots','code term','','1','SG','3.3.1 Functional Intent, PDF p26 L2001','Designated accessible vehicle parking lots must be provided on a proportional basis solely for the use by persons with disabilities.',''),
 ('R2-050','Accessible carparking spaces','code term','"carparking" is written as one word throughout the AU text (orthographic variant)','1','AU','Sch 1 D3.5, PDF p36 L2045','Accessible carparking spaces:',''),
 ('R2-050','Carparking spaces for use by people with a disability','code term','performance-requirement wording of the same space','1','AU','Sch 1 DP8 (heading "Carparking for people with a disability"), PDF p29 L1536','Carparking spaces for use by people with a disability must be:',''),
 ('R2-050','accessible parks','colloquial','NZ noun "park" for a parking space; here inside a COMMENT pointing to NZS 4121','1','NZ','10.1.1 COMMENT, PDF p48 L3340','the number of accessible parks to be provided',''),
 ('R2-050','accessible car parking','code term','','1','NZ','10.1.1 COMMENT, PDF p48 L3339','NZS 4121 in section 5 covers the provision of accessible car parking',''),
 ('R2-050','designated car-parking spaces','code term','defined by the permit: spaces for holders of a disabled person\'s parking permit','1','IE','1.1.3, PDF p33 L1159','designated car-parking spaces (exclusively for the use of holders of a disabled person’s parking permit)',''),
 ('R2-050','designated car parking spaces','regional variant','unhyphenated spelling of the previous row in the same instrument (orthographic)','1','IE','1.1.5, PDF p50 L1322','designated car parking spaces are those spaces exclusively provided for the holders of a disabled person’s parking permit',''),
 ('R2-050','Designated accessible parking','code term','','1','B651','9.4 (heading), p. 230','Designated accessible parking',''),
 ('R2-050','Designated accessible parking spaces for limited mobility users','code term','B651 carves a second class (R2-051); listed here only to show the shared head noun','1','B651','9.5 (heading), p. 236','Designated accessible parking spaces for limited mobility users','B651 9.4 and 9.5 use one head form for two classes of space'),
 # ---------- parking: tier 2 statutes ----------
 ('R2-050','handicapped parking','outdated or disfavoured',HANDI,'2','NY','§ 1203-b(1)','in any area designated as a place for handicapped parking',''),
 ('R2-050','Parking spaces for the handicapped','outdated or disfavoured',HANDI,'2','NY','§ 1203-b(1)','Parking spaces for the handicapped as provided for in sections one thousand two hundred three-a',''),
 ('R2-050','handicapped parking permit','outdated or disfavoured',PARK_PERMIT+'. '+HANDI,'2','NY','§ 1203-b(1)','accorded to a holder of a handicapped parking permit',''),
 ('R2-050','disabled persons parking bay','code term','statutory definition keyed to the permit','2','IESI','art. 2 (definitions), text L181','"disabled persons parking bay" means a space intended for the parking of a mechanically propelled vehicle',''),
 ('R2-050','Disabled Persons Parking Bay','code term','name of road traffic sign RRM 015','2','IESI','art. 44(1), text L427','where traffic sign number RRM 015 [Disabled Persons Parking Bay] is provided',''),
 ('R2-050','disabled person’s badge','code term',PARK_PERMIT,'2','UKBADGE','reg. 2 to 9, text L4','a disabled person’s badge shall be issued for a period of three years',''),
 ('R2-050','parking for people with disabilities','code term','title of the regulations; names the provision, not a bay','2','WA','title, text','Local Government (Parking for People with Disabilities) Regulations 2014',''),
 ('R2-050','disability parking permit','code term',PARK_PERMIT,'2','WA','reg. 3 (definitions), text L39','disability parking permit means a current document issued by National Disability Services',''),
 ('R2-050','ACROD Parking Program Card','product name',PARK_PERMIT+'; ACROD is the WA programme name','2','WA','reg. 3, text L41','an ACROD Parking Program Card;',''),
 ('R2-050','accessible parking permit','code term',PARK_PERMIT,'2','ON581','s. 2 and following, text L43','The Minister shall issue an accessible parking permit for use related to travel',''),
 ('R2-050','Accessible Parking for Persons with Disabilities','code term','title of the regulation','2','ON581','title','R.R.O. 1990, Reg. 581: ACCESSIBLE PARKING FOR PERSONS WITH DISABILITIES',''),
 ('R2-050','Accessible Parking Space','code term','','2','TOR','200.15.1 (1), text L56','Accessible Parking Space Dimensions (Minimum)',''),
 # ---------- parking: tier 3 signage ----------
 ('R2-050','RESERVED PARKING for persons with disabilities','code term','legend of sign R7-8','3','MUTCD','Section 2B.46, text L2257','RESERVED PARKING for persons with disabilities (R7-8);',''),
 ('R2-050','parking spaces that are reserved for persons with disabilities','code term','','3','MUTCD','Section 2B.46 para 08, text L2299','Where parking spaces that are reserved for persons with disabilities are designated to accommodate wheelchair vans',''),
 ('R2-050','VAN ACCESSIBLE','code term','NARROWER: plaque R7-8P below R7-8','3','MUTCD','Section 2B.46, text L2258','VAN ACCESSIBLE (R7-8P);',''),
 ('R2-050','Parking for disabled badge holders only','code term',PARK_PERMIT,'3','KYTS','on-street parking signs, text L118','Parking for disabled badge holders only, at all times.',''),
 ('R2-050','reserved for disabled badge holders','code term',PARK_PERMIT,'3','KYTS','on-street parking bays, text L207','the bay is reserved for disabled badge holders only',''),
 ('R2-050','Disabled Badge Holders Only','code term',PARK_PERMIT+'; Northern Ireland sign','3','NI','publication title, text L17','Disabled Badge Holders Only At All Times Sign',''),
 # ---------- parking: tier 4 public bodies ----------
 ('R2-050','Blue Badge','product name',PARK_PERMIT+'; the scheme name, not a statutory term in SI 2000/682 as made','4','GOVBB','page body, text L85','Find out where Blue Badge holders can park','GB public pages use the scheme name ("Blue Badge") where the regulations say "disabled person’s badge"'),
 ('R2-050','Accessible Parking Spaces','code term','','4','USAB','"Minimum Number of Accessible Parking Spaces", text L94','Minimum Number of Accessible Parking Spaces',''),
 ('R2-050','van accessible spaces','code term','NARROWER','4','USAB','"Van Accessible Parking Spaces", text L341','van accessible spaces can share a common access aisle',''),
 ('R2-050','Disabled Person Parking Placards','code term',PARK_PERMIT,'4','CADMV','page title, text L68','Disabled Person Parking Placards & Plates',''),
 ('R2-050','persons with disabilities parking','colloquial','attributive form on a public page','4','CADMV','text L114','Next to a blue curb authorized for persons with disabilities parking.','"blue curb" names the painted kerb marking a disabled-person space; curb as marking, not as the street edge or the ramp'),
 ('R2-050','Accessible parking','code term','the recommended form in US language guidance','4','ADANN','"Use / Don\'t Use" table, text L2','Use Don’t Use Accessible parking Handicapped parking',''),
 ('R2-050','Handicapped parking','outdated or disfavoured','listed under "Don\'t Use". '+HANDI,'4','ADANN','"Use / Don\'t Use" table, text L2','Note that ‘handicapped’ is an outdated and unacceptable term to use',''),
 ('R2-050','marked disabled parking bay','colloquial','','4','DARWIN','PDF p1 L5','To park in a marked disabled parking bay',''),
 ('R2-050','disabled bay','colloquial','short form in a council table','4','DARWIN','PDF p2 L53','Marked disabled bay:',''),
 ('R2-050','Accessible Parking Spaces','code term','','4','BELL','heading, text L173','Accessible parking spaces help people with mobility challenges park closer to shops',''),
 ('R2-050','Mobility Parking Scheme (MPS) permit','product name',PARK_PERMIT+'; NSW scheme name','4','BELL','text L175','You must display a valid Mobility Parking Scheme (MPS) permit to use these spaces.',''),
 ('R2-050','accessibility parking','colloquial','owner-supplied form, here attested on a public library page','4','DAREBIN','text L40','wheelchair access, accessibility parking, accessible toilets, and more.',''),
 ('R2-050','Accessibility Parking Permit','colloquial',PARK_PERMIT+'; Victoria\'s permit is not confirmed by a statute read here','4','DAREBIN','text L49','If you have an Accessibility Parking Permit, you will find accessible parking spaces','one page uses "accessibility parking" and "accessible parking spaces" for one object'),
 ('R2-050','disabled parking spaces','colloquial','','4','GLEN','text L86','wheelchair travel passes or disabled parking spaces, we can help.',''),
 ('R2-050','accessible parking lots','code term','','4','SGEG','text L84','Vehicles that display a valid Car Park Label can park in accessible parking lots',''),
 ('R2-050','Car Park Label','product name',PARK_PERMIT+'; SG scheme name','4','SGEG','text L84','display a valid Car Park Label',''),
 ('R2-050','disabled car park lots','colloquial','','4','MSF','title, text L1','HDB season parking for disabled car park lots','the same reply also says "accessible parking lots" and "accessible lot": two forms, one object, one page'),
 ('R2-050','accessible parking space','code term','','4','ONAPP','text L82','to park in an accessible parking space',''),
 ('R2-050','barrier-free parking spaces','code term','Ontario zoning usage; owner-supplied "barrier free parking" attested here','4','SSM','s. 5.5.1, PDF p2 L63','SURFACE TREATMENT OF REQUIRED BARRIER-FREE PARKING SPACES',''),
 ('R2-050','mobility parking spaces','code term','','4','UOA','text L380','Mobility parking spaces are available within the building car park',''),
 # ---------- parking: tier 5 disability organisation ----------
 ('R2-050','mobility parks','colloquial','NZ form; the organisation is a disability service and advocacy body, whether disabled-people-led is not established here','5','CCS','FAQ heading, text L151','Using mobility parks and permits',''),
 ('R2-050','accessible parks','colloquial','','5','CCS','FAQ, text L152','your Mobility Parking Permit allows you to access the accessible parks','equates the "mobility" permit with "accessible" parks: two qualifiers, one space'),
 # ---------- parking setting ----------
 ('R2-281','parking facility','code term','the US Standards chose it over "parking lot" to cover garages','1','US','Advisory 208.2 (text L797)','The term “parking facility” is used Section 208.2 instead of the term “parking lot”',''),
 ('R2-281','carpark','code term','AU defined term: a building for parking','1','AU','Sch 1 A1.1 definitions, PDF p19 L990','carpark means a building that is used for the parking of motor vehicles','AU "carpark" is a building; SG/UK "car park" is any parking area'),
 ('R2-281','car parks','code term','','1','UK','1.17, PDF p20 L1948','multi-storey car parks.',''),
 # ---------- access aisle ----------
 ('R2-053','access aisle','code term','','1','SG','3.3.1, PDF p24 L1952','provide an access aisle of at least 1200 mm wide',''),
 ('R2-053','parking access aisles','code term','','1','US','28 CFR 35.151 path of travel (text L210)','parking access aisles; elevators and lifts;',''),
 ('R2-053','accessibility zone','code term','UK name of the zone between bays; equivalence judged by sense (the clear zone beside the bay)','1','UK','1.18 b, PDF p20 L1958','with a 1200mm accessibility zone between',''),
 ('R2-053','accessible barrier free aisle','code term','two umbrella qualifiers stacked on one noun','2','TOR','200.15.1, text L72','adjacent to a 1.5 metre wide accessible barrier free aisle or path','"accessible" and "barrier free" used together as one qualifier'),
 # ---------- passenger loading ----------
 ('R2-052','Passenger Loading Zones','code term','','1','US','503 (text L117)','503 Passenger Loading Zones',''),
 ('R2-052','setting down point','code term','','1','UK','1.18 e, PDF p20 L1983','a clearly sign-posted setting down point',''),
 ('R2-052','Passenger Alighting and Boarding Points','code term','includes taxi shelters in SG','1','SG','contents 3.4, PDF p3 L103','Passenger Alighting and Boarding Points, including Taxi Shelters',''),
 ('R2-052','On–Site Setting Down Areas','code term','','1','IE','1.1.6 (contents), PDF p3 L74','On–Site Setting Down Areas',''),
 # ---------- curb ramps ----------
 ('R2-059','Kerb Ramps','regional variant','','1','SG','contents, PDF p3 L124','Changes in Levels and Kerb Ramps',''),
 ('R2-059','Kerb ramp','regional variant','defined term','1','NZ','Definitions, PDF p15 L763','Kerb ramp means a short ramp either cutting',''),
 ('R2-059','dropped kerbs','regional variant','','1','IE','1.1.5, PDF p50 L1318','tactile paving and dropped kerbs',''),
 ('R2-059','kerb ramp','regional variant','','1','AU','Sch 1 D3.8, PDF p39 L2321','if there is no kerb or kerb ramp at that point',''),
 # ---------- accessible route ----------
 ('R2-072','Accessible Routes','code term','','1','US','206 (text L55)','206 Accessible Routes','US route includes elevators and platform lifts (forms.tsv note)'),
 ('R2-072','Accessible Routes','code term','','1','SG','contents 3.1, PDF p3 L117','Accessible Routes, Corridors and Paths',''),
 ('R2-072','Access Routes','code term','the NZ clause name','1','NZ','title, PDF p1 L4','D1 Access Routes',''),
 ('R2-072','Access Routes','code term','','1','IE','1.1.3 (contents), PDF p3 L71','1.1.3 Access Routes',''),
 ('R2-072','access routes','code term','','1','UK','contents, PDF p3 L152','Hazards on access routes',''),
 ('R2-074','accessible path of travel','code term','AU term; defined in AS 1428.1, not obtained','1','AU','Part 4 s 4.1, PDF p8 L405','provide a continuous accessible path of travel from the entrance to the new part.','US "path of travel" (28 CFR 35.151(b)(4)) is an alterations term, not this route (pass record carve 4)'),
 ('R2-074','accessways','code term','AU operative noun','1','AU','PDF p10 L534','(a) accessways',''),
 # ---------- vision panels ----------
 ('R2-156','Vision Lights','regional variant','','1','US','404.2.11 (text L1746)','404.2.11 Vision Lights.',''),
 ('R2-156','vision panels','regional variant','','1','UK','index, PDF p66 L6070','Doors – vision panels',''),
 ('R2-156','Vision Panels','regional variant','','1','SG','Figure 28, PDF p6 L434','Figure 28 Vision Panels',''),
 # ---------- elevator ----------
 ('R2-163','destination-oriented elevator','code term','NARROWER: a control-system subclass','1','US','407.2.2.4 (text L1863)','Each destination-oriented elevator in a bank of elevators',''),
 ('R2-163','Private Residence Elevators','code term','NARROWER: restricted class','1','US','409 (text L112)','409 Private Residence Elevators',''),
 ('R2-163','passenger lift','code term','','1','UK','3.17, PDF p34 L3312','3.17 A passenger lift is the most suitable',''),
 ('R2-163','passenger lift','code term','','1','IE','2.3 (text), PDF p76 L1719','A passenger lift is the most accessible means of vertical',''),
 ('R2-163','Passenger lifts','code term','UMBRELLA in AU: the table of "types of passenger lifts" includes platform lifts','1','AU','Sch 1 E3.6, Table E3.6(a), PDF p47 L2772','Limitations on use of types of passenger lifts','AU lists "Low-rise platform lift" and "Inclined lift" as types of passenger lift (Table E3.6(a)): R2-163 and R2-168 under one form'),
 ('R2-163','lift car','code term','the car, R2-165 sense, used with lift','1','UK','3.33, PDF p36 L3475','Where planning allows, lift cars',''),
 ('R2-163','Passenger elevator','code term','Ontario regulatory class','2','ON209','s. 38 (heading), text L468','Every owner of a passenger elevator shall ensure that,',''),
 ('R2-163','Elevators and Platform Lifts','code term','US guidance keeps the two nouns apart in one chapter title','4','USAB','navigation, text L55','Chapter 4: Elevators and Platform Lifts',''),
 ('R2-163','lifts','colloquial','','4','DAREBIN','text L42','we have ramps or lifts available to facilitate easy access for all patrons.',''),
 # ---------- elevating devices ----------
 ('R2-164','Elevating devices','code term','','1','B651','5.6 (heading), p. 125','Elevating devices',''),
 ('R2-164','Lifting devices','code term','UK index class over passenger lifts and platform lifts','1','UK','index, PDF p68 L6560','Lifting devices – passenger lifts',''),
 ('R2-164','lifting devices','code term','','1','IE','2.3, PDF p76 L1735','Consideration should be given to other lifting devices, such as lifting platforms',''),
 ('R2-164','elevating devices','code term','O. Reg. 209/01 classes: elevators, dumbwaiters, escalators, moving walks, platform and material lifts, lifts for persons with physical disabilities','2','ON209','s. 2 classes, text L195','6. Lifts for persons with physical disabilities, being,',''),
 # ---------- platform lifts ----------
 ('R2-168','lifting platforms','code term','IE uses "platform lift" and "lifting platform" for one device','1','IE','2.3, PDF p76 L1737','Lifting platforms should comply with 2.3.4.1.1.',''),
 ('R2-168','platform lift','code term','','1','IE','1.1.3, PDF p33 L1151','Alternatively, a platform lift may be provided',''),
 ('R2-168','enclosed vertical platform lifts','code term','NARROWER subclass; also "unenclosed vertical platform lifts"','2','ON209','s. 2 class 6 iv, text L199','iv. enclosed vertical platform lifts, and',''),
 ('R2-168','Lifts for persons with physical disabilities','code term','Ontario class over platform and stair lifts; also the pre-2019 CSA B355 title (search S5, not retrieved)','2','ON209','s. 2 class 6, text L195','6. Lifts for persons with physical disabilities, being,','one class name covers R2-168 and R2-169'),
 ('R2-168','Wheelchair lifts','colloquial','vehicle-mounted van lift in a US advisory, NOT a building platform lift','1','US','Advisory 502 (text L2063)','Wheelchair lifts typically are installed on the passenger side of vans','"wheelchair lift" names a vehicle device here; the building device is "platform lift" (410)'),
 # ---------- stair lifts ----------
 ('R2-169','Wheelchair platform stairlifts','code term','','1','UK','3.44, PDF p38 L3699','3.44 Wheelchair platform stairlifts are only',''),
 ('R2-169','Wheelchair Stairlifts','code term','','1','SG','4.10 (contents), PDF p3 L133','4.10 Platform Lifts and Wheelchair Stairlifts',''),
 ('R2-169','stair chair lifts','code term','NARROWER: a seat, distinct from a stair platform lift','2','ON209','s. 2 class 6 i, text L196','i. stair chair lifts,','Ontario separates stair chair lifts from stair platform lifts; the register row does not'),
 ('R2-169','enclosed stair platform lifts','code term','NARROWER','2','ON209','s. 2 class 6 ii, text L197','ii. enclosed stair platform lifts,',''),
 # ---------- single accessible toilet room ----------
 ('R2-177','unisex wheelchair-accessible toilet','code term','single-user room; equivalence to RHFAC 5.3 judged by the single-user sense, not by the qualifier','1','UK','1.? contents/0.?, PDF p11 L1036','wheelchair-accessible unisex toilet and a',''),
 ('R2-177','universal toilets','code term','Approved Document T type, cited from ADM','1','UK','0.? (Part T note), PDF p11 L1045','equipment of universal toilets and singlesex toilets','"universal" names a toilet type, as in RHFAC 5.3, not the umbrella qualifier'),
 ('R2-177','accessible individual washroom','code term','','1','SG','5.? , PDF p63 L4258','A standalone wheelchair-accessible washroom (accessible individual washroom)',''),
 ('R2-177','Unisex accessible toilet','code term','','1','AU','Sch 1 F2.4, PDF p65 L3765','Unisex accessible toilet',''),
 ('R2-177','Wheelchair accessible unisex WC','code term','','1','IE','1.4.5 (contents), PDF p4 L101','1.4.5 Wheelchair accessible unisex WC',''),
 ('R2-177','Accessible restroom','colloquial','recommended US form; room type unstated','4','ADANN','"Use / Don\'t Use" table, text L2','Accessible restroom Disabled restroom','"Disabled restroom" is listed under Don\'t Use'),
 # ---------- symbol ----------
 ('R2-208','International Symbol of Access for Persons with Disabilities','code term','','1','SG','figure list, PDF p4 L239','International Symbol of Access for Persons with Disabilities',''),
 ('R2-208','international symbol of access','code term','','1','AU','Sch 1 D4, PDF p37 L2181','incorporate the international symbol of access or deafness',''),
 ('R2-208','white wheelchair symbol on a blue square','colloquial','a description of the symbol in a sign manual','3','MUTCD','Section 2B.46, text L2299','a white wheelchair symbol on a blue square',''),
 ('R2-208','BARRIER-FREE SYMBOL','code term','Ontario zoning name for the symbol','4','SSM','Amendment 2 heading, PDF p2 L60','AMENDMENT 2 –BARRIER-FREE SYMBOL',''),
 # ---------- the umbrella qualifier ----------
 ('R2-333','Accessible','qualifier','US defined term: compliance with the Standards','1','US','106.5 definitions (text L496)','Accessible. A site, building, facility, or portion thereof that complies with this part.',''),
 ('R2-333','accessible and inclusive','qualifier','"inclusive" paired with "accessible"; SG also names "Universal Design principles"','1','SG','Introduction, PDF p8 L660','requirements for accessible and inclusive buildings.',''),
 ('R2-333','barrier-free','qualifier','','1','SG','2.?, PDF p21 L1792','must provide barrier-free connectivity',''),
 ('R2-333','Universal Design','qualifier','WIDER: defined by the Disability Act 2005, a design approach','1','IE','0.1 Introduction, PDF p13 L401','underpin the principle of Universal Design.',''),
 ('R2-333','inclusive','qualifier','','1','IE','0.1 Introduction, PDF p13 L397','Part M aims to foster an inclusive approach',''),
 ('R2-333','accessible building','qualifier','AU attaches the umbrella word to a building class','1','AU','Sch 1 E3.6, PDF p47 L2763','In an accessible building, every passenger lift must:',''),
 ('R2-333','barrier-free','qualifier','statutory long title of the federal act','2','ACA','long title, text L124','An Act to ensure a barrier-free Canada',''),
 ('R2-333','handicapped','outdated or disfavoured',HANDI,'2','NY','§ 1203-b heading','§ 1203-b. Parking spaces; handicapped.',''),
 ('R2-333','disabled','qualifier','UK government guidance prefers "disabled people"; US guidance lists "Disabled restroom" under Don\'t Use','4','NORTH','PDF p2 L59','(the) handicapped; the disabled; the disabled people or disabled person','UK guidance lists "people with disabilities" to AVOID and "disabled people" to USE; US guidance (ADANN) the reverse for spaces'),
 ('R2-333','wheelchair-friendly','qualifier','NARROWER: wheelchair users only; owner-supplied form attested on a council page','4','BELL','text L167','such as wheelchair-friendly paths, toilets, parking spaces, and key services.',''),
 ('R2-333','wheelchair-accessible','qualifier','NARROWER','4','BELL','text L106','amenities include wheelchair-accessible toilets, ramps, handrails, and designated parking spaces.',''),
 ('R2-333','Singapore Association of the Visually Handicapped','product name','organisation name carrying "handicapped"; '+HANDI,'1','SG','acknowledgements, PDF p116 L7166','Singapore Association of the Visually Handicapped',''),
]
def norm(s): return re.sub(r'\s+', ' ', s).strip()
cache = {}; bad = 0; out = []
for c, form, ut, sc, tier, sk, loc, q, conf in R:
    t, iss, jur, url, tf = S[sk]
    p = os.path.normpath(os.path.join(D, tf))
    if p not in cache: cache[p] = norm(open(p, encoding='utf-8', errors='replace').read())
    ok = norm(q) in cache[p] and len(q.split()) <= 25 and norm(form).lower() in cache[p].lower()
    if not ok: bad += 1; print('FAIL', c, form, '|', q, file=sys.stderr)
    out.append([c, L[c], form, 'en', jur, ut, sc, tier, f'{t} — {iss} — {url}', loc, q, conf])
with open(os.path.join(D, 'equivalents.tsv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['concept_id','concept_label','form','language','jurisdiction','usage_type','scope_note','attestation_tier','source','locator','quote','conflation_note'])
    w.writerows(out)
print(f'{len(out)} rows, {bad} failures'); sys.exit(1 if bad else 0)
