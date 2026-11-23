#!/usr/bin/env python3
"""Ensure every script in assign.json has inserts covering >=10% of est_seconds (2 s each, build100 plays a fixed 2.0 s).
Adds story inserts to non-comic scripts, forces seconds=2, and repairs after_line values that build100 would silently drop.
build100: flip is placed at 0-based line index after_line+1; index n-1 is the outro -> valid after_line is 0..n-3, unique.
Only 'inserts' is written. Idempotent. Backup: scripts.bak_inserts/ (created once)."""
import json, os, math, shutil, sys
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SD = f"{H}/scripts"; BK = f"{H}/scripts.bak_inserts"
if not os.path.exists(BK): shutil.copytree(SD, BK)
FLAT = "generic cartoon characters"
# no -> [(L, characters, story)] ; L = 1-based line the 2 s cutaway illustrates (after_line = L-2 per build100)
N = {
2:[(3,"generic cartoon scout","A cartoon scout dozes in an armchair at home beside a giant video tape on a small TV. Gag: he presses play with his toe and tiny cartoon players wave from the screen. Twist: he gives a thumbs-up, then a sticky note on the tape reads Be kind, rewind."),
   (5,"caricature of Shevchenko","A caricature of Shevchenko lifts a golden ball trophy next to a giant video tape in a gold frame. Gag: he kisses the tape. Twist: the tape ejects a tiny ticket reading 24 goals.")],
5:[(2,"generic cartoon teams","A cartoon scoreboard shows 2-0 while the team in dark shirts relaxes on deck chairs. Gag: three rival players sprint in and fire three balls into the net while a tiny espresso cup bounces. Twist: the scoreboard flips to 2-3 and the espresso spills."),
   (5,"caricature of Cannavaro","A caricature of Cannavaro sips a tiny espresso at a coffee bar while a wall calendar shows ten days. Gag: the calendar pages flip away like a fast fan. Twist: the barista yawns, very slowly pushing over the next cup.")],
8:[(2,"generic cartoon club president; caricature of Kaka","A cartoon club president pushes a wheelbarrow stacked with gold coins toward a caricature of Kaka in a white shirt. Gag: the wheelbarrow tips and coins roll everywhere. Twist: Kaka catches one coin, smiles politely and pockets it."),
   (5,"generic cartoon referee; caricature of Kaka","A cartoon referee raises a yellow card in front of a caricature of Kaka. Gag: the referee raises a second yellow right after, and a stopwatch behind them shows only 18 minutes. Twist: Kaka checks his wristwatch, nods and strolls off quickly.")],
11:[(2,"generic cartoon coach; caricature of Messi","A cartoon coach hands a caricature of Messi a clipboard and a whistle. Gag: Messi studies the clipboard upside down, then tucks a football under his arm. Twist: the whistle rolls into his pocket and he gives a tiny shrug."),
    (6,"caricature of Messi","A caricature of Messi stands on a podium holding a giant golden boot. Gag: he gently puts the boot down next to last year's boot and the two are twins. Twist: a pair of cartoon assistants try to hand him a clipboard and he points at the boots.")],
17:[(2,"generic cartoon pundit","A cartoon pundit in a studio chair stares into a crystal ball that shows a tiny trophy. Gag: the ball fills with a chart pointing downward. Twist: the crystal ball cracks and the pundit gives a confident thumbs-up anyway."),
    (5,"generic cartoon pundit; cartoon fox with a crown","A cartoon pundit holds a storybook open on a hill. Gag: a tiny fox in a crown pops out of the book and does a victory dance. Twist: the pundit closes the book, whispering, and the fox waves from the cover.")],
26:[(3,"caricature of Ronaldinho; generic cartoon goalkeeper","A caricature of Ronaldinho lines up a free kick from far outside the box. Gag: the ball curves in a huge looping arc over a cartoon goalkeeper's gloves. Twist: the goalkeeper is still looking at the wall, then the net bulges and he turns."),
    (4,"generic cartoon referee; caricature of Ronaldinho","A cartoon referee lifts a red card toward a smiling caricature of Ronaldinho. Gag: he skips off the pitch waving to the crowd. Twist: the tunnel opens on a cosy bathtub with a rubber duck, and he hops in.")],
29:[(5,"caricature of Kane","A caricature of Kane carries a golden ball trophy to a tall museum glass case. Gag: the case is too small, so he squeezes the trophy in and then himself. Twist: a cartoon guard taps the glass and Kane gives a tiny wave from inside."),
    (6,"caricature of Kane","A caricature of Kane lines up a penalty. Gag: the ball clangs off the crossbar with a huge ringing bell sound and the bar shakes. Twist: the ball rebounds into his hands and he sighs.")],
31:[(2,"generic cartoon chairman","A cartoon chairman spins on a swivel chair beside a coach-shaped figure on a rack. Gag: he swaps the figure for an identical one and spins again. Twist: the nameplate on the desk flips to a new name in the blink of an eye."),
    (4,"generic cartoon team and keeper","A cartoon stadium clock reads 39 and the scoreboard shows 0-3. Gag: a cartoon goalkeeper empties the net of three balls with a shovel. Twist: a fourth ball pops in right after he finishes.")],
32:[(2,"generic cartoon team in white shirts","A cartoon team in white shirts rings the doorbell of a huge stadium door. Gag: a chain of 43 links hangs across the entrance and they snip it with giant scissors. Twist: the door opens and a surprised cartoon bull in a red shirt waves hello."),
    (4,"generic cartoon teenage winger","A generic cartoon teenage winger with a school backpack dribbles past two defenders. Gag: he sets up two team-mates with perfect passes, one after another. Twist: a cartoon alarm clock rings and he checks his homework planner.")],
33:[(2,"generic cartoon red-shirt team and fans","A cartoon scoreboard shows 0-2 with the clock at 18 minutes and the red-shirt fans sink in their seats. Gag: the fans pull out umbrellas against a rain of cartoon gloom clouds. Twist: a tiny sun peeks out from behind the scoreboard."),
    (5,"generic cartoon calendar","A cartoon calendar page is covered with nine red crosses in a row. Gag: a hand stamps a big green tick over the next square. Twist: the crosses all pop off and bounce away like confetti.")],
34:[(2,"generic cartoon shopkeeper; tiny cartoon midfielder","A cartoon shopkeeper hands a tiny cartoon midfielder over a counter for a small bag of coins. Gag: the price tag on the midfielder flips from 6 to 80 as the boy grows taller. Twist: the shopkeeper stares at the tag, then at his coins, and hugs the player to buy him back."),
    (4,"generic cartoon radio host","A cartoon radio on a shelf crackles with sound waves. Gag: a cartoon cleaner dusts under it and hears a whisper from the speaker. Twist: a tiny suitcase pops out of the radio and rolls toward the door.")],
36:[(2,"generic cartoon striker","A cartoon striker climbs a tall ladder made of golden balls above a stadium. Gag: below, his club stands in a dim basement with a tiny rescue rope. Twist: he stops at the top and drops a rope down to them."),
    (5,"generic cartoon scouts","Cartoon scouts with binoculars lean out of many windows of one tall building. Gag: they bump heads and their binoculars tangle together. Twist: a huge price tag swings down in front of them and they all gulp.")],
37:[(2,"generic cartoon players and referee","A cartoon player falls in the box and a cartoon referee points firmly at the spot. Gag: the ball rolls onto the spot and trembles with nerves. Twist: the penalty goes in and the stands erupt with confetti."),
    (6,"generic cartoon coach","A cartoon coach sits at his desk under a dark cloud with a stack of paperwork. Gag: a gift-wrapped box lands on his desk from a passing blue-shirt kit man. Twist: inside is a tiny cup labelled with a smiley face, and the cloud turns into a sun.")],
38:[(3,"generic cartoon club sellers","Two cartoon clubs haggle at a market stall with a price board showing 2 and 7. Gag: the gap between them stretches into a deep canyon with a rope bridge. Twist: the seller shakes his head three times in a row."),
    (6,"caricature of De Bruyne","A shelf holds six golden trophies. Gag: a caricature of De Bruyne slaps a small price sticker on each, one by one. Twist: the last sticker says Bargain and a customer in a hurry runs off with the whole shelf.")],
39:[(2,"generic cartoon goalkeeper and players","A cartoon shot dribbles slowly toward a goalkeeper. Gag: the ball squirms under his body like a mouse. Twist: it crawls into the net and the keeper looks at his empty gloves."),
    (6,"generic cartoon coach and fans","A cartoon coach stands at a microphone in front of a crowd of cartoon fans giving thumbs down. Gag: he bows with a tiny blame sign over his head. Twist: the crowd's thumbs all flip up for one second, then down again.")],
40:[(3,"generic cartoon defenders and winger","A cartoon winger runs at goal while two defenders still pull their boots on, each hopping on one leg. Gag: the winger passes between them without breaking stride. Twist: he shoots and the ball lands in the net before the defenders' boots are on."),
    (4,"generic cartoon striker and defender","A cartoon striker shoots toward goal and the ball bounces off a defender's knee. Gag: a second shot is a simple tap-in from one centimetre. Twist: both balls roll into the net and the keeper takes a bow anyway.")],
41:[(3,"generic cartoon players on a balance scale","A giant balance scale has eleven cartoon players on one side and ten on the other. Gag: the ten side sinks lower and the scale creaks. Twist: the eleven side flies up and lands on top of the scale's pole."),
    (5,"generic cartoon coach with a team sheet","A cartoon coach holds up a team sheet with a question mark in the defender's spot. Gag: a cartoon detective with a magnifying glass studies the sheet. Twist: a hidden defender pops out of the sheet's folded corner and waves.")],
42:[(2,"generic cartoon investor in a sports jacket","A cartoon investor in a sports jacket walks out through a stadium door carrying a tiny slice of pie. Gag: behind him a league table board flips and the home team slides up to the top. Twist: he looks back, puzzled, and the pie slice is wearing sunglasses."),
    (5,"generic cartoon pie chart","A giant pie chart sits on a boardroom table with a tiny sliver of 3.3 percent. Gag: the sliver stands up, puts on a tiny hat and bows. Twist: the rest of the chart applauds with little hands."),
    (7,"generic cartoon chairman and young striker","A cartoon chairman pushes a wheelbarrow of coins toward a young striker with a record-breaking price tag. Gag: the coins pile higher than the chairman. Twist: the striker waves and the pile of coins turns into a tower of golden balls.")],
45:[(3,"generic cartoon red-shirt club and cartoon defender","A cartoon red-shirt club holds a big coin on a string labelled Option, not a rope. Gag: the string stretches like elastic as the defender tugs back and forth. Twist: the coin pings off and bounces into a piggy bank."),
    (5,"generic cartoon defender with a captain's armband","A cartoon defender with a captain's armband sits on a bench under cobwebs. Gag: a tiny spider hangs a banner above him. Twist: the spider shyly offers him a sandwich and he accepts."),
    (8,"generic cartoon defender and voting box","A cartoon defender holds a single ballot slip beside a big ballot box. Gag: a pair of cartoon clubs with price tags crowd around the box. Twist: he drops his slip in and the clubs all lean in to read it.")],
47:[(3,"generic cartoon winger","A cartoon winger scores three goals while a giant stopwatch hand races around a tiny dial. Gag: three balls land in a tiny net labelled with a small island flag. Twist: the stopwatch shows 21 and the winger blinks in surprise."),
    (5,"generic cartoon winger","A cartoon winger walks off the pitch with a substitution board above his head. Gag: he crosses his arms and sulks with a tiny storm cloud overhead. Twist: under his arm he is still holding all three match balls.")],
48:[(2,"generic cartoon owner","A cartoon owner plants a big For Sale sign on a stadium roof. Gag: the sign's price tag is blank and he scratches his head. Twist: a tiny question mark floats out of the tag and takes a seat."),
    (4,"generic cartoon coaches in a revolving door","A cartoon revolving door spins out coach after coach in identical tracksuits. Gag: the door spins faster and faster until the coaches blur. Twist: a stack of eleven name tags falls out of the door in a heap."),
    (5,"generic cartoon owner and suitcase","A cartoon owner packs a stadium into a rolling suitcase. Gag: the stadium's roof sticks out and he sits on the case to close it. Twist: the suitcase grows wheels and rolls away with the owner holding on.")],
50:[(2,"generic cartoon teenage striker and goalkeeper","A generic cartoon teenage striker takes a calm shot against a tall cartoon goalkeeper. Gag: he chips the ball high over the goalkeeper's raised gloves. Twist: the ball dips under the bar and the striker shrugs without apology."),
    (3,"generic cartoon bench of legends","A short stone bench holds three shadowy cartoon legends in a row. Gag: a generic cartoon teenager sits on the end and the bench creaks. Twist: the bench grows a fourth seat and everyone scoots over to make room.")],
51:[(3,"caricature of Rapinoe","A caricature of a cartoon footballer with short bright hair walks through a grand front door of a glittering hall. Gag: she carries a golden ball trophy and tips her hat. Twist: the door closes behind her and a red carpet unrolls ahead."),
    (6,"caricature of Beckham","A caricature of a cartoon midfielder with a swept hairstyle tiptoes through a side door of the same hall. Gag: he straightens his tie at the last second. Twist: the side door opens into the same golden hall and he beams.")],
52:[(2,"generic cartoon team in white shirts","A cartoon scoreboard rolls from 0 to 5 in the blink of an eye. Gag: five different cartoon scorers pop up one by one with raised arms. Twist: the scoreboard shows 5-0 and a tiny orange rival waves a very small white flag."),
    (4,"generic cartoon team and stopwatch","A cartoon stopwatch hand rushes around a dial from one to eleven. Gag: three goals land in the net as the hand races. Twist: the Dutch defence runs off the pitch toward a cartoon coffee van."),
    (6,"caricature of a cartoon coach with a cap and glasses","A caricature of a cartoon coach with a cap and glasses and a huge grin hugs an invisible friend. Gag: he shushes a crowd of doubters with a finger to his lips. Twist: the doubters wave back and tiptoe out.")],
53:[(2,"generic cartoon team","A cartoon team climbs a giant ladder labelled with numbers up to 77. Gag: at the top a golden ball waits on a pedestal. Twist: the ladder rungs add one more step and the ball moves up with them."),
    (4,"generic cartoon defenders and goalkeeper","A cartoon defensive wall stacks into a big castle. Gag: the goalkeeper waves a flag from the highest tower. Twist: a rival cartoon striker knocks at the castle door and the drawbridge stays up.")],
54:[(2,"generic cartoon giants and cartoon teen","Two cartoon giants in different shirts play tug-of-war with a cartoon teenage defender as the rope. Gag: the rope stretches like elastic. Twist: the teen floats away on a balloon and both giants fall over."),
    (6,"generic cartoon seller","A relaxed cartoon seller lies in a deckchair beside a stall with a giant price tag. Gag: a line of cartoon clubs waits and checks their watches. Twist: the seller sips lemonade and flips the tag one number higher.")],
55:[(3,"generic cartoon giants and cartoon fullback","Two cartoon giants wave from opposite sides at a cartoon fullback on a bench. Gag: they hold up price signs with a 40. Twist: the fullback politely waves back and points at the bench cushion."),
    (6,"generic cartoon fullback","A cartoon fullback sits on a bench with a cushion and a book. Gag: a cartoon coach points at a tiny field far away. Twist: the bench grows a throne back and he sits like a king.")],
57:[(2,"caricature of Hakimi","A caricature of Hakimi wears a magician's top hat on the pitch. Gag: he pulls three balls out of the hat, one after another. Twist: two more doves fly out carrying assist signs."),
    (4,"caricature of Hakimi","A tiny cartoon piggy bank labelled with the number two sits on a shelf for a very long time. Gag: dusty cobwebs gather and a clock ticks 135. Twist: the piggy bank bursts open with five golden balls.")],
58:[(2,"generic cartoon linesman and striker","A cartoon linesman lifts a flag again and again until seven flags make a bouquet. Gag: a cartoon striker offside each time looks at the camera. Twist: the linesman hands the bouquet to the striker as a gift."),
    (3,"generic cartoon striker and defender","A cartoon striker shoots and the ball hits a defender's knee. Gag: it loops over the keeper in slow motion. Twist: the ball drops into the net and the keeper sits down on the grass."),
    (6,"generic cartoon coach","A cartoon coach in a dark suit runs to the touchline. Gag: he slides on his knees across wet grass for a long, long time. Twist: he finishes at the corner flag and takes a bow.")],
60:[(3,"generic cartoon goalkeeper","A cartoon goalkeeper tries to catch a ball covered in soap bubbles. Gag: the ball slips out and spins in the air. Twist: it drops into the net and he looks at his soapy gloves."),
    (5,"generic cartoon coach and alarm clock","A cartoon coach sleeps in a big bed on the touchline. Gag: a huge alarm clock rings and the coach pulls a pillow over his head. Twist: the whole team is still in pyjamas.")],
62:[(3,"generic cartoon winger","A cartoon winger lies in a beach hammock with a tiny trophy beside him. Gag: a stopwatch ticks and a calendar flips. Twist: a whistle blows and he jumps up in full kit holding a suitcase."),
    (5,"generic cartoon coach","A cartoon coach holds up two big signs, one with a thumbs-up and one with a thumbs-down. Gag: he flips them back and forth. Twist: the thumbs-up wears a smile and the thumbs-down wears a frown.")],
63:[(2,"generic cartoon team","A cartoon net bulges as nine balls drop in one after another. Gag: the goalkeeper tries to count them on his fingers and runs out of fingers. Twist: he puts on a second pair of gloves to keep counting."),
    (5,"generic cartoon coach and players","A cartoon coach holds a finger to his lips as a crowd of cheering players inflates a giant balloon. Gag: the balloon grows bigger than the stadium. Twist: the coach pokes it with a tiny pin and it deflates with a gentle sigh.")],
64:[(2,"generic cartoon players and a VAR screen","A cartoon scoreboard shows 0-2 early in the match. Gag: a huge cartoon VAR screen with a glowing eye rises above the stadium. Twist: the eye blinks and looks at the striker."),
    (4,"generic cartoon VAR screen and referee","A cartoon referee watches a VAR monitor with a magnifying glass over a hand. Gag: the glass slides along the arm and stops on the hand. Twist: a tiny arrow points at the hand and the referee points to the spot."),
    (5,"generic cartoon striker","A cartoon striker whips off his shirt in celebration. Gag: the referee raises a yellow card in a flash. Twist: he is wearing a second shirt and keeps celebrating.")],
65:[(2,"generic cartoon teen winger","A cartoon teenage winger sits on a bench with a tiny flag. Gag: he waves the flag at the pitch with a hopeful look. Twist: a tiny bird lands on his flag and he whispers hello."),
    (3,"generic cartoon coach with peg","A cartoon manager holds a winger-shaped peg beside a formation board with a square hole. Gag: he tries to push the peg into the hole and it won't fit. Twist: the peg rotates into a perfect shape and clicks in.")],
66:[(3,"generic cartoon player","A cartoon player lines up from far out. Gag: the ball launches like a rocket and leaves a long trail of sparks. Twist: it hits the top corner and the net sparkles."),
    (4,"generic cartoon egg timer","A cartoon egg timer shows three minutes of sand. Gag: the sand falls and the net bulges at the other end. Twist: the timer flips back and the scoreboard shows 1-1.")],
68:[(2,"generic cartoon federation office","A cartoon federation office has a wall poster with a silhouette and a big question mark. Gag: a cartoon clerk pins the poster upside down. Twist: the question mark rolls off the poster and down the corridor."),
    (4,"generic cartoon coach and yoghurt","A cartoon coach signs a contract beside a small yoghurt pot with a stopwatch. Gag: he lifts a corner of the contract and the pot's date is later than his term. Twist: the yoghurt shrugs and he waves goodbye.")],
71:[(3,"generic cartoon midfielder","A cartoon midfielder in black and white stripes winds up a long shot. Gag: the ball curves in a spiral toward the top corner. Twist: the net ripples and the crowd flips from boos to cheers."),
    (5,"generic cartoon referee","A cartoon referee shows a second yellow to a player in light-blue. Gag: the player shrugs and trudges off. Twist: the referee hands the player a tiny umbrella for the walk.")],
73:[(2,"generic cartoon coach with price tag","A cartoon coach wears a big price tag that reads 5. Gag: a cartoon clerk scans the tag with a beeping scanner. Twist: the scanner prints a receipt a mile long."),
    (5,"generic cartoon coach and relay baton","A cartoon coach is handed a tiny relay baton on the touchline. Gag: he runs with it for one step. Twist: he passes it to another coach, who passes it to a third."),
    (6,"generic cartoon coach and podium","A cartoon coach hops from the third step of one podium to the third step of another. Gag: he almost slips. Twist: the two podiums are the same and the coach shrugs.")],
75:[(2,"generic cartoon striker","A cartoon striker scores a late winner as the clock shows 78. Gag: the net bulges and a flurry of confetti falls. Twist: the confetti forms a number 14."),
    (5,"generic cartoon striker and touches counter","A cartoon striker's boot touches the ball thirteen times in a row, each marked by a number pop. Gag: the boot jumps and the numbers pile up like coins. Twist: the thirteenth touch is a goal."),
    (6,"generic cartoon striker with whiteboard","A cartoon striker stands at a whiteboard in front of his team-mates. Gag: he draws a big arrow that says More. Twist: team-mates salute and the arrow points at the ball.")],
76:[(2,"generic cartoon team","Five different cartoon scorers pop up in a row, each with a different shirt number. Gag: each one waves and the scoreboard ticks up. Twist: the fifth one is still wearing a tracksuit."),
    (4,"generic cartoon fans","Cartoon fans hold up a big banner with a question mark. Gag: the banner swings left and right as the crowd sways. Twist: the question mark turns into an exclamation mark and a tiny drum starts."),
    (5,"generic cartoon coach","A cartoon coach bows politely toward the crowd. Gag: a bouquet of cartoon flowers lands at his feet. Twist: he picks it up and gives it back.")],
77:[(2,"generic cartoon film owners","Two cartoon owners in sunglasses sit in director's chairs at a pitch side. Gag: a cartoon clapperboard snaps in front of them. Twist: the chairs collapse and they land in a heap."),
    (3,"generic cartoon players","A late ball loops into a crowded penalty box. Gag: a cartoon midfielder jumps and heads it down. Twist: it bounces over the line and the scoreboard reads 1-1."),
    (7,"generic cartoon team and staircase","A cartoon team climbs a long staircase with leagues on each step. Gag: a cartoon camera crew follows them step by step. Twist: at the top a golden door opens onto a bright spotlight.")],
78:[(2,"generic cartoon table ladder","A cartoon league table is a ladder with team figures climbing it. Gag: a small club hops up past a big club with a smile. Twist: the big club drops a rung and waves goodbye."),
    (4,"generic cartoon referee and VAR monitor","A cartoon VAR monitor shows a replay with a red card icon. Gag: the referee runs to the monitor and checks it. Twist: the red card pops out of the screen."),
    (7,"generic cartoon team counting","A cartoon team counts its players on its fingers. Gag: it reaches ten and starts over. Twist: the eleventh player is hiding behind the ball.")],
80:[(2,"generic cartoon team and goalkeeper","A cartoon pie chart shows 57 percent possession and one shot. Gag: the team holds a ball with both arms and does not shoot. Twist: a rival taps in a goal and the pie chart laughs."),
    (4,"generic cartoon team","A cartoon team celebrates a late win with a pile of gold coins. Gag: the coins spill across the floor. Twist: the pile spells a very large number two.")],
81:[(2,"generic cartoon teen defender and trophy","A cartoon trophy shaped like a striker looks surprised as a teenage defender receives it. Gag: the trophy tries to climb away and the defender holds it tight. Twist: the trophy gives up and sits on his shoulder."),
    (4,"generic cartoon trophy shelf","A conveyor belt delivers four trophies to a shelf one by one. Gag: each trophy wears a different tiny shirt. Twist: the fifth trophy arrives and the shelf says Full.")],
82:[(2,"generic cartoon director and door","A cartoon director knocks on a giant door. Gag: the door opens a crack and a hand pushes him back. Twist: the door slams and a Keep Out sign pops up."),
    (4,"generic cartoon defender and contract tree","A cartoon defender stands rooted like a tree holding a contract scroll. Gag: roots grow from his boots into the grass. Twist: a tiny bird builds a nest on the scroll.")],
83:[(2,"generic cartoon coin wheelbarrow","A cartoon club official wheels a barrow stacked with 70 coins up to a gate. Gag: the coins turn into a tall tower. Twist: the gate opens and a different winger walks out."),
    (3,"generic cartoon winger","A cartoon winger arrives wearing a bright shirt on the right wing. Gag: the left wing stays empty with a lonely chair. Twist: a tiny sign on the chair reads Reserved.")],
85:[(2,"generic cartoon fullback","A cartoon fullback sits on a bench with a thought bubble showing a golden ball. Gag: the bubble floats upward. Twist: a pin pops it with a soft squeak."),
    (4,"generic cartoon bench","A cartoon bench has a name tag and a cushion with a dent. Gag: a spider spins a web across it. Twist: the spider uses the web as a hammock."),
    (5,"generic cartoon crossing machine","A cartoon crossing machine fires balls to the box with number counters. Gag: it spins and fires 64 balls. Twist: a cartoon fullback catches the last one and bows.")],
86:[(2,"generic cartoon giant club and winger","A cartoon giant peeks through a curtain at a young winger. Gag: the curtain rips and the giant freezes. Twist: the winger waves hello and the giant pretends to be a statue."),
    (5,"generic cartoon winger shop window","A cartoon winger stands in a shop window while cartoon clubs press their noses on the glass. Gag: their noses make big squashed prints. Twist: the winger pulls down a blind.")],
92:[(2,"generic cartoon clubs and winger","Six cartoon fishermen cast lines toward one small winger. Gag: the lines tangle into a single knot. Twist: the winger swims away holding a price tag."),
    (5,"generic cartoon clubs","Six cartoon clubs stand in a row each holding a number. Gag: they all shout their numbers together. Twist: the winger holds up one finger and the numbers vanish.")],
95:[(2,"caricature of Guimaraes","A caricature of Guimaraes knocks on the door of his old stadium wearing a new shirt. Gag: the door opens and a doorman squints at the shirt. Twist: the doorman waves him in and hands him a cup of tea."),
    (5,"generic cartoon coach and vending machine","A cartoon coach feeds a coin into a praise vending machine. Gag: one tiny compliment drops out at a time. Twist: the machine says Come back tomorrow.")],
98:[(2,"generic cartoon analyst","A cartoon analyst hides behind a hedge with binoculars. Gag: a dog sniffs the hedge and he squeaks. Twist: the hedge is a cartoon cloud and he floats away."),
    (4,"generic cartoon scoreboard","A cartoon scoreboard starts with a big minus four. Gag: a team adds points one at a time. Twist: a tiny hand rubs out the minus and the board resets.")],
}
def need(est): return 3 if 4.0/est < 0.10 else 2
def fix_lines(ins, n):
    """Return after_line values valid for build100 (0..n-3), unique, order preserved."""
    hi = n-3; used=set(); out=[]
    for x in ins:
        a=min(max(x["after_line"],0),hi)
        while a in used and a>0: a-=1
        if a in used:
            a=next((b for b in range(hi+1) if b not in used),a)
        used.add(a); out.append(a)
    return out
log=[]
A={a["no"]:a for a in json.load(open(f"{H}/scripts/assign.json"))}
for no in sorted(A):
    p=f"{SD}/{no:03d}.json"; raw=open(p,encoding="utf-8").read(); j=json.loads(raw)
    n=len(j["lines"]); ins=j.get("inserts",[]); changed=False
    if not j.get("comic") and len(ins)<need(j["est_seconds"]):
        assert no in N, f"no stories for {no}"
        ins=[{"after_line":L-2,"story":s,"characters":c,"seconds":2} for L,c,s in N[no][:need(j["est_seconds"])]]
        for L,_,_ in N[no][:need(j["est_seconds"])]: assert 2<=L<=n-1,(no,L,n)
        changed=True
    for i in ins:
        if i.get("seconds")!=2: i["seconds"]=2; changed=True
    new=fix_lines(ins,n)
    if new!=[i["after_line"] for i in ins]:
        log.append((no,[i["after_line"] for i in ins],new))
        for i,a in zip(ins,new): i["after_line"]=a
        changed=True
    if changed:
        j["inserts"]=sorted(ins,key=lambda i:i["after_line"])
        out=json.dumps(j,indent=1,ensure_ascii=("\\u" in raw))+("\n" if raw.endswith("\n") else "")
        json.loads(out); open(p,"w",encoding="utf-8").write(out)
print("after_line repaired:",len(log)); [print(" ",l) for l in log]
