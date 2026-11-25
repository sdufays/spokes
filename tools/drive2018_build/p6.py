import csv
OUT='/Users/Sarah/spokes/raw/drive/2018/'
rows=[]
def add(name,org,cat,role,email='',phone='',city='',outcome='',src='',link=''):
    rows.append([name,org,cat,role,email,phone,city,2018,outcome,src,link])
L=lambda i:f"https://docs.google.com/spreadsheets/d/{i}/edit"
# team
ci=("Contact Info",L('1gBqmG4LiO1gznNsgaUKlF0oO4U58oO_f2dfdH87Vawk'))
for n,e,p in [("Bethany Cates","bcates@mit.edu","(716)553-1763"),("Delia Stephens","delias@mit.edu","(512)289-6476"),("An Jimenez","jimeneza@mit.edu","(469)571-8487"),("Kate Pearce","kpearce@mit.edu","(224)567-2524"),("Annie Phan","anniephan96@gmail.com","(512)785-7660"),("Alex Tran","alextran@mit.edu","(832)466-1172"),("Matthew Luerman","mluerman@mit.edu","(760)212-8480"),("Lisa Peng","lisapeng@mit.edu","(973)462-2756")]:
    add(n,"MIT","rider-alum","Spokes 2018 rider",e,p,"Cambridge, MA","",*ci)
# alumni
al=("Spokes Alumni sheet",L('11xgXmXkUNitP-2qguI0iAkI2tl9cVIRa6Seo4vpYv1o'))
A="""2017|MIT/Harvard|Caity Looby|crlooby@mit.edu||Cambridge, MA|mentor yes
2017|MIT/Harvard|Thi Bui|thibui@mit.edu||Cambridge, MA|mentor yes
2017|MIT/Harvard|Cody Winkleblack|cwinkleb@mit.edu||Cambridge, MA|
2017|MIT/Harvard|Olivia Siegel|osiegel@mit.edu||Cambridge, MA|can help
2017|MIT/Harvard|Javi Gutierrez|javier.gutierrez@college.harvard.edu||Cambridge, MA|
2017|MIT/Harvard|Masha Karelina|maschka@alum.mit.edu||San Ramon, CA|
2017|MIT/Harvard|Margalit Glasgow|margalit.r.glasgow@gmail.com||Cambridge, MA|2017 team lead per notes; mentor yes
2017|Stanford|Stephanie Zhang|szhang3@stanford.edu||Palo Alto, CA|
2017|Stanford|Angela Kong|akong2@stanford.edu||Palo Alto, CA|
2017|Stanford|Margaret Shen|margaretshen100@gmail.com||San Francisco, CA|
2017|Stanford|Maddy Fish|madfish@stanford.edu||Palo Alto, CA|
2017|Stanford|Kevin Penner|kpenner@stanford.edu||Palo Alto, CA|
2017|Stanford|Hasna Rtabi|hasna@stanford.edu||Palo Alto, CA|
2017|Stanford|Vince Ranganathan|akranga@stanford.edu||Palo Alto, CA|
2016|MIT/Harvard|Antonis Michael|antonism@mit.edu||Cambridge, MA|
2016|MIT/Harvard|Nhat (Nick) Nguyen|nvn@mit.edu|||
2016|MIT/Harvard|Jean Chow|j.chow.0305@gmail.com|||
2016|MIT/Harvard|Annie Wei|anniewei@mit.edu|||
2016|MIT/Harvard|Omar Embaby|omarembaby@college.harvard.edu|||
2016|MIT/Harvard|Yang Dai|Ydai144@gmail.com|||
2016|MIT/Harvard|Noam Ben-Tzur|noambentzur21@gmail.com|||
2016|MIT/Harvard|Chloe Yang|cjwyang@mit.edu||Cambridge, MA|
2015|MIT/Harvard|Tola Omilana|tola.omilana@gmail.com||Los Angeles, CA|mentor yes; no updates
2015|MIT/Harvard|Francesca Childs|francesca.childs@gmail.com|802-579-3336|Vail, CO|
2015|MIT/Harvard|Simon Shuham|simonshuham@gmail.com||Denver, CO|
2015|MIT/Harvard|Brian Wagner|bwagner@college.harvard.edu||Cambridge, MA|
2015|MIT/Harvard|Shadi Fadaee|shadifadaee@alumni.harvard.edu||Iran|
2015|MIT/Harvard|Drew Bent|bent@mit.edu|650-862-6270|Cambridge, MA|
2015|MIT/Harvard|Jorge Troncosco|jatron@mit.edu||Cambridge, MA|mentor yes
2014|MIT/Harvard|Emma Benjaminson|benjaminsonemma9@gmail.com|617-710-5393|LA, CA|mentor yes
2014|MIT/Harvard|Maddie Hickman|madeline.hickman@gmail.com||Boston, MA|mentor yes
2014|MIT/Harvard|Jamin Liu|c.jamin.liu@gmail.com|857-399-6023|Berkeley, CA|mentor yes
2014|MIT/Harvard|Jace Warner|cali.j.warner@gmail.com|||does not want contact
2014|MIT/Harvard|Caleb Fujimori|caleb.fujimori@gmail.com||Palo Alto, CA|no mentor
2014|MIT/Harvard|Evan Gastman|evangastman@gmail.com|||
2014|MIT/Harvard|Sam Green|green.sam1192@gmail.com|||can help
2013|MIT|Turner Bohlen|turnerbohlen@gmail.com|508-202-2866|Olympia, WA|
2013|MIT|Claire O'Connell|cl.ella.oco@gmail.com||New York, NY|mentor yes
2013|MIT|Philip Daniels|pdaniel@alum.mit.edu||Cambridge, MA|no mentor
2013|MIT|Titiaan Palazzi|titiaan.palazzi@gmail.com||Aspen, CO|mentor yes; also $20+ 2018 crowdfund donor
2013|MIT|Jeff Prouty|jcprouty@gmail.com||Cambridge, MA|
2013|MIT|Nathan Kennedy|nkkennedy13@gmail.com||Berkeley, CA|
2013|MIT|Ethan Sherbody|sherbondye@gmail.com||Cambridge, MA|mentor yes
2013|MIT|Kaitlyn Bailey|kbailey0831@gmail.com||Berkeley, CA|"""
for l in A.split('\n'):
    y,t,n,e,p,c,note=l.split('|')
    r=[n,f"Spokes {y} {t}","rider-alum",f"Spokes {y} rider ({t}); {note}".strip('; '),e,p,c,y,"",*al]; rows.append(r)
# sponsors
ps=("Potential Sponsors sheet",L('1qsDkL3jXGkFt0Qut2d04N-CipduKbod6GnV1p2vs0hU'))
S=[("Texas Instruments","sponsor","Delia outreach","","said no"),("MathWorks","sponsor","Delia outreach; listed as 2017 major contributor","","replied; no amount recorded"),("Garmin","sponsor","web form 3/31/2018","","no award recorded"),("Sony","sponsor","not accepting donations; letter submitted 4/20","","said no"),("Nikon","sponsor","must apply 6 months before program","","cancelled"),("GoPro","sponsor","only sponsors athletes","","cancelled"),("IAT Interactive","sponsor","contact Kaitlin Tyler, Senior Media Coordinator","",""),("COOLA Suncare","sponsor","Kate","","samples secured"),("Outdoor Research","sponsor","sponsorship@outdoorresearch.com","sponsorship@outdoorresearch.com","email sent 3/29"),("Timbuk2","sponsor","web form (link broken)","","form sent 3/29"),("Kelty","sponsor","form 3/24; reviewed quarterly","","form sent"),("Platypus (Cascade Designs)","sponsor","sponsorship form","",""),("REI","sponsor","An; asked $10,000","","email 4/6"),("Camelbak","sponsor","An","","email 4/6"),("Arc'Teryx","sponsor","An","","email 4/6"),("Heartbreak Hill Running Company","sponsor","An","","email 4/6"),("Landry's Bicycle","bike-shop","Delia; quoted Specialized Diverge/Trek CrossRip","","reached out; bikes bought elsewhere"),("Belmont Wheelworks","bike-shop","donation form","","reached out"),("Back Bay Bicycles","bike-shop","","","reached out"),("Ace Wheelworks","bike-shop","","",""),("Bicycle World","bike-shop","An","","email 4/6"),("Wheelworks","bike-shop","offered Diverge Sport A1 at $1,000/bike + 15% off gear","","not chosen"),("Cambridge Bicycle (259 Massachusetts Ave; 617-876-6555; contact Benjamin Smart)","bike-shop","sold 8 Jamis Renegade Exile","","bought bikes $7,185.53"),("Giant World","bike-shop","quoted","","not chosen"),("Community Bike Supply","bike-shop","emailed 4/9","",""),("Ford Motor Company Fund","sponsor","van grant request $6,000","","no award recorded"),("Koch Foundation","sponsor","$5,000 request letter","","no outcome recorded"),("Dell (MSDF)","sponsor","grant application","","no outcome recorded"),("MakeCrate","sponsor","Delia's mother's company; donated electronics kits","","donated kits"),("Systems & Technology Research (STR)","donor","600 West Cummings Park, Woburn MA; str-recruiting@stresearch.com","str-recruiting@stresearch.com","donated $500")]
for n,c,r,e,o in S: add(n,n,c,r,e,"","",o,*ps)
for n,e,co,note,st in [("Elizabeth Bowers","ebowers@alum.mit.edu","Intel","interested in K-12 education","emailed 4/24, no response"),("Ramin Baghai","rbaghai@alum.mit.edu","Google","Head of Marketing","not yet contacted"),("Cheryl Texin","ctexin@alum.mit.edu","National Instruments","Austin","replied, said interested"),("Tom Bales","tombales@alum.mit.edu","Syntheon","CTO",""),("Robyn Allen","nybor@alum.mit.edu","Startup","Cycling Club alum","emailed 4/21"),("David Godbe Anderson","dga@cs.cmu.edu","Carnegie Mellon","CS prof; Cycling Club + MITOC","emailed 4/21"),("Koji Asari","kasar@alum.mit.edu","GE","Cycling Club","emailed 4/21"),("Zachary Bailey","zbailey@alum.mit.edu","JPL","Cycling Club","emailed 4/21"),("Megan Smith","megans@gmail.com","Formerly Google","former US CTO","emailed 4/24")]:
    add(n,co,"donor",f"MIT alum prospect; {note}",e,"","",st,*ps)
for n,e,st in [("MIT Club of Chicago","mitclubofchicago@alum.mit.edu","gave $500"),("MIT Club of Western New York","","emailed 4/24"),("MIT Club of Austin and San Antonio","","no response"),("MIT Club of Northern NJ (carol.tourgee@alum.mit.edu)","carol.tourgee@alum.mit.edu","emailed 4/30"),("Massiah (Maseeh) Foundation","","contacted 4/30; unlikely")]:
    add(n,n,"donor","alumni club / foundation",e,"","",st,*ps)
for n,o,e,r in [("John Brisson","MIT Course 2","brisson@mit.edu","dept; gave $750 per budget"),("Chiamaka Agbasi-Porter","MIT Lincoln Labs","chiamaka.porter@llab.mit.edu",""),("William Litant","MIT Course 16","wlitant@mit.edu","Communications Director"),("Jaime Peraire","MIT Course 16","peraire@mit.edu","Department Head; $0"),("Nicholas Roy","MIT Course 16","nickroy@mit.edu","Delia's advisor"),("David Miller","MIT Course 16","","Matthew's advisor"),("Peter Fisher","MIT Course 8","fisherp@mit.edu","Department Head; gave $2,500"),("Sandi Lipnoski","Edgerton Center","slipnosk@mit.edu","Edgerton staff; budget/van quote/reimbursement contact"),("Chris Mayer","Edgerton Center","mayerc@mit.edu","Edgerton staff"),("Angie Belcher","pk-12 Action Group","belcher@mit.edu","asked for any help"),("Daniel Darling","MIT Course 20","","Communications + Outreach"),("Asuman (Course 6 dept head)","MIT Course 6","asuman@mit.edu","gave $2,000"),("Course 7 Development + Giving","MIT Course 7","degriff@mit.edu",""),("Cynthia Barnhart","MIT","","donor $2,000 per Projected Costs")]:
    add(n,o,"mit-staff",r,e,"","Cambridge, MA","",*ps)
for n,u in [("WBZ","newstips@wbztv.com"),("WCVB",""),("WBTS/NBC Boston",""),("WFXT Fox25",""),("NECN",""),("KVUE","news@kvue.com"),("KXAN",""),("KEYE","news@cbsaustin.com"),("Fox 7 / KTBC","KTBCnews@foxtv.com"),("Austin American-Statesman","newstips@statesman.com")]:
    add(n,n,"press","news tip sent",u,"","","sent",*ps)
add("Mr. McGrory","Boston Globe","press","pitch email by Kate","","","Boston, MA","no coverage recorded","Boston Globe doc","https://docs.google.com/document/d/1W_DG4m4I2KPRQAKJJjTEWObOFzGOuFj8FdPQU3cTods/edit")
add("Mr. Litchman","(MIT alum)","donor","personal-network grant request letter by Kate","","","","unknown","Kate's Letter to Mr. Litchman","https://docs.google.com/document/d/1JGl8ufHOIViJMYDcVsodFWhwtG40iFulImYobe_asUg/edit")
# hosts / schools
rt=("2018 Route sheet",L('1t2rcDZ0FMIpyMKqpSBLPsGQnvz2FZbaVwVCBoxtDKb0'))
def h(y,n,cat,role,phone,city,out): rows.append([n,"",cat,role,"",phone,city,y,out,*rt])
h(2018,"Elizabeth Snyder","host","Warmshowers, 5017 25th St N","(703)798-1051","Arlington, VA","hosted us (DC, rest day)")
h(2018,"Pohick Bay Regional Park Campground","campground","6501 Pohick Bay Dr","","Lorton, VA","stayed May 29")
h(2018,"Bruce and Vikki White","host","Warmshowers, 10400 Dynasty Ct","(540)379-1181","Fredericksburg, VA","hosted us 2017 and 2018")
h(2018,"Ingrid Claire Martin","host","Warmshowers, commune, 1259 Indian Creek Rd","(978)257-5865","Mineral, VA","hosted us")
h(2018,"Jonathan T. Hine","host","Warmshowers, 1708 Concord Dr (likely unavailable next year)","(434)960-1344","Charlottesville, VA","hosted us")
h(2018,"Francine Johnston","host","Warmshowers, 709 Jefferson Ave","(336)202-9413","Waynesboro, VA","hosted us 2017 and 2018")
h(2018,"Marilyn Buerkens","host","Warmshowers, 5146 Plank Rd (chores expected)","(540)319-8607","Natural Bridge, VA","hosted us")
h(2017,"Cindy Gray","host","15535 Laurel Ridge Rd","703-680-3629","Montclair, VA","hosted 2017")
h(2017,"Beth Evans","host","4609 Burnley Station Rd (steep gravel drive)","434-981-4785","Barboursville, VA","hosted 2017")
h(2017,"Wendy and Mike Orrison","host","495 This Way","540-570-2383","Natural Bridge Station, VA","hosted 2017")
h(2017,"Alta Mons campground","campground","2842 Crockett Springs Rd; $15/site","540-268-2409","Shawsville, VA","stayed 2017")
h(2017,"Mark Smith (and neighbors Stacy and Mike)","host","845 N 20th St","276-920-0656","Wytheville, VA","neighbors hosted 2017")
h(2017,"John and Patty Brenner","host","Warmshowers, 246 B Street SE","276-701-7243 / 276-701-7244","Abingdon, VA","hosted 2015, 2016, 2017")
h(2017,"Donnie Sorah","host","314 Oakwood Ave SE","276-393-2426","Wise, VA","hosted 2017")
h(2015,"Sherry Spradlin","host","Harmony House Bed and Breakfast, owner","606-477-3231","Hazard, KY","hosted 2015, 2016")
h(2016,"Camp Bethel Ministries","host","church summer camp, very helpful","","Wise, VA","hosted 2016")
h(2016,"Natural Bridge/Lexington KOA","campground","800-562-8514, $44","800-562-8514","Natural Bridge, VA","stayed 2015, 2016")
h(2016,"Crabtree Falls Campground","campground","","540-377-2066","Tyro, VA","stayed 2015, 2016")
h(2015,"Soniya Carvalho","host","former Uruguayan embassy in DC","","Washington, DC","hosted 2015")
sc=("Potential Schools sheet",L('1DjQTxDQYF6IZHsNgO1f5tsvXQiBaymGlBKoO7k6fkr4'))
for n,o,r,e,p,c,out in [("(contact not listed)","Louisa County Public Library","","","","Mineral, VA","festival June 1, 2018"),("Tom Cravens","Challenger Learning Center of Kentucky","1 Community College Dr","tom.cravens@kctcs.edu","","Hazard, KY","festival June 13-14 (2-day, strong connection)"),("Ann Boes","Lab: Revolution (makerspace)","3276 Jerome Ave","annboes2007@gmail.com","573-327-2009","Farmington, MO","festival June 23-24"),("Ashlea Appelbaum","St. Louis Home School Connection","Lafayette Park UMC, 2300 Lafayette Ave","creativeappel@gmail.com","","St. Louis, MO","festival June 26"),("William Wells","aSTEAM Village","1600 Paseo Blvd, 64108","william@asteamvillage.org","","Kansas City, MO","festival July 2"),("Marianne Eichelberger","Newton Public Library","720 North Oak, 67114","meichelb@newtonplks.org","","Newton, KS","festival July 5"),("Beth Gudmestad","Loveland Public Library","300 North Adams","Beth.Gudmestad@cityofloveland.org","","Loveland, CO","festival July 14"),("Mr. Porter","Christa McAuliffe Space Center","Central Elementary, 95 North 400 East","spacecenter@alpinedistrict.org","","Pleasant Grove, UT","festival July 21; 100 HS kids in 2017"),("(K. Babcock)","Carson City Public Library","900 N Roop St, 89701","KBabcock@carson.org","","Carson City, NV","July 31-Aug 1; only 11 attended in 2017")]:
    rows.append([n,o,"lf-partner",r,e,p,c,2018,out,*sc])
# crowdfund donors
cf=("$50+ Letter Recipients",L('1xtBK-Syg9ZFbcUgK04uIEKh8esni3QFcEA2gBWYWYTw'))
D="""Jose Jimenez|josejc27@sbcglobal.net|Dallas, TX|100
Steven Larky|larky@alum.mit.edu|Del Mar, CA|100
Debbie and Michael Rubashkin|dkr23466@aol.com|Barrington, IL|75
Tony Peng|tpeng85@gmail.com|San Francisco, CA|100
Sharon Massey|smassey@springstreet.org|Friday Harbor, WA|50
Kay Knowles|kayaskay@outlook.com|San Jose, CA|100
Don and Ilene Kramer|dkramer@nhcmail.com|Houston, TX|100
Khatantuul Filer|kzorig30@gmail.com|Cambridge, MA|50
Anh Pise|anhpise@gmail.com|Richmond, TX|75
Howard Reubenstein|hbr@alum.mit.edu|Bedford, MA|100
Roberta Cates|roberta.cates@yahoo.com|Buffalo, NY|100
Marie Cox|marie.cox@outlook.com|Fairfax, VA|50
Jesus del Alamo|alamo@mit.edu|Lincoln, MA|100
Kelly Liu|kellybean0809@gmail.com|Acton, MA|50
Norma Hannigan|normitahannigan@yahoo.com|Newburgh, NY|50
Stephanie Stephens|steph_stephens@hotmail.com|Austin, TX|100
Matt Hodel|beyondtheacheron@gmail.com|Wilton, CT|50
Cory Schillaci|cdschillaci@gmail.com|Berkeley, CA|50
Sanford Nobel|s.nobel@alum.mit.edu|Williamsville, NY|100
James Stephens|jstephens@tribblestephens.com|Bertram, TX|500
Robert Floyd|rfloyd@hslawmail.com|Austin, TX|100
Cathy Glover|cdg4224@yahoo.com|New York, NY|500
Holt Newton|holtnewton@sbcglobal.net|Round Rock, TX|100
Kaabao Yang|kaabaoyang@gmail.com|San Francisco, CA|100
Pearce Family|spearces@aol.com|Glencoe, IL|100
Michelle Hardy|michellehardy89@gmail.com|Plano, TX|50
Deborah Pearce|debzpearce@gmail.com|Jackson, NJ|100
Simon Verghese|simonverghese@gmail.com|Mountain View, CA|100
Lynne Katzmann|lynne.katzmann@junipercommunities.com|Upper Montclair, NJ|100
Rita McComber|rmccomber@ameritech.net|Appleton, WI|60
Cathy Thompson|csthomp16@comcast.net|Belle Mead, NJ|50"""
for l in D.split('\n'):
    n,e,c,a=l.split('|'); rows.append([n,"","donor","2018 MIT crowdfund donor",e,"",c,2018,f"donated ${a}",*cf])
cf2=("$20+ Email List",L('1gQ6YbujiI3b9EKHicwJ3nRF7MPFXOSqbG0wFD_oqU-s'))
known={r[4] for r in rows}
for e in "elizabeth_s_bray@hotmail.com mbamama07@yahoo.com carol24je@yahoo.com mritchie99@gmail.com liuyang.lisa@gmail.com nick.dillman@gmail.com boleary@livingston.org stacyhmo@gmail.com cskier@alum.mit.edu adahuang@mit.edu susan.udin@gmail.com sthom479@aol.com lawrencescott19@gmail.com rsheppard817@gmail.com rogers.roddy@roadrunner.com lauren@spoonfilms.com tiffanyy9968@gmail.com bloyd@me.com harry@hairycow.name sjm1@usa.net janellejsmith@yahoo.com dgguys@comcast.net heinsolid@gmail.com".split():
    rows.append(["","","donor","2018 crowdfund donor ($20+ tier)",e,"","",2018,"donated $20+",*cf2])
with open(OUT+'_contacts.csv','w',newline='') as f:
    w=csv.writer(f,quoting=csv.QUOTE_MINIMAL)
    w.writerow("name,organization,category,role_or_notes,email,phone,city_state,year,outcome,source_file,source_link".split(','))
    # map 'press'->press
    for r in rows:
        if r[2]=='press': pass
        w.writerow(r)
print(len(rows))
