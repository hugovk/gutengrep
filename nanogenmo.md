gutengrep poetry generator
--------------------------

Riffing on a suggestion made in #55, I wrote a script to grep full sentences using regexes from the Project Gutenberg CD. It uses NTLK to find full sentences rather than the arbitrary lines in a file that grep finds. It can also sort them by shortest sentence first.

But first.

The OED has a word of the day email, and the quotations for "moonlit" struck me as particularly poetic:

> Along the moon-lit shore,—a dreary waste,—no peaceful Indian watch'd her rising orb.
> Night silent comes;..Tilt half enchains wi' rugged hand His moon-lit wave.
> The City's moon-lit spires and myriad lamps.
> The sloping of the moonlit sward.
> She stood on deck, watching the moonlit sea.
> He was crazy in love with her and one moonlit night he proposed to her.
> The sky was clear and moonlit and cold.
> She stood looking out at the shadowed grey-white moonlit world.
> Below her the wall dropped dizzyingly down,..and beyond that the moonlit roofs of the outer city reached away.

Moonlit
=======

Let's try this on Project Gutenberg. There are 597 text files on the CD containing 3,583,390 sentences.

> A moonlit nightcall: far, far.

> from that moonlit cedar what a burst!

> It was now a beautiful, moonlit night.

> Let you stay here in the moonlit garden!

> Perhaps they all come back on moonlit nights.

...

> Walking among the sleeping birds in the hedges, watching the skipping
rabbits on a moonlit warren, or standing under a pheasant-laden bough,
she looked upon herself as a figure of Guilt intruding into the haunts
of Innocence.

> He loved driving his spirited horses along the lonely, moonlit roads,
and she loved to sit on the box-seat, with the soft air of an English
late summer's night fanning her face after the hot atmosphere of a
ball or supper-party.

> He had seen her lying at her length quietly, her black hair scattered
on the pillow, like shadow of twigs and sprays on moonlit grass,
illuminated intermittently; smiling to him, but her heart out and
abroad, wild as any witch's.

Once upon a time
================

Let's search for "once upon a time":

> We were engaged once upon a time.

> It was delightful once upon a time!

> "Once upon a time" -- "Well, go on."

> Once upon a time, the Foxes were angry with Sun.

> Once upon a time this had been a dream of the future.

...

> Once upon a time we knew country life so well and city life so little,
that we illustrated city life as that of a closely crowded country
district.

> A Malay poem relates how once upon a time in the city of Indrapoora
there was a certain merchant who was rich and prosperous, but he had
no children.

> THE FISH AND THE RING Once upon a time, there was a mighty baron in
the North Countrie who was a great magician that knew everything that
would come to pass.


And then!
=========

Or "And then" at the start of each sentence (regex: `[^\w]*And then`):

> And then?

> And then?

> And then!

...

> And then as we looked the white figure moved forwards again.

> And then there was nothing further to be said on the matter.

> And then adieu to prudence and virtue, honour and fair fame.

...

> And then her thoughts flew back to her old predictions, and the number
of times she had said, that Kate with no fortune would marry better
than other people's daughters with thousands; and, as she pictured
with the brightness of a mother's fancy all the beauty and grace of
the poor girl who had struggled so cheerfully with her new life of
hardship and trial, her heart grew too full, and the tears trickled
down her face.

> And then when the repast is over and the tables removed, for the
knight to recline in the chair, picking his teeth perhaps as usual,
and a damsel, much lovelier than any of the others, to enter
unexpectedly by the chamber door, and herself by his side, and begin
to tell him what the castle is, and how she is held enchanted there,
and other things that amaze the knight and astonish the readers who
are perusing his history.

But why?
========

Or "But why" at the start of each sentence (regex: `[^\w]*But why`):

> But why?

> But why?

...

> "But why not?"

> "But why, WHY?"

> "But why, man?"

> But why a year?

...

> But why, like infants, cold to honour's charms, Stand we to talk, when
glory calls to arms?

> But why should they be so set against him, since they also despise the
way that he forsook?

...

> But why may not a man also argue, on the contrary, that it is the
effect of a precipitous and insatiate spirit not to know how to bound
and restrain its coveting; that it is to abuse the favours of God to
exceed the measure He has prescribed them: and that again to throw a
man's self into danger after a victory obtained is again to expose
himself to the mercy of fortune: that it is one of the greatest
discretions in the rule of war not to drive an enemy to despair?

Happily ever after
==================

Not many, so here's the full thing:

> Then he took possession of the place and lived happily ever after.

> The woman was discharged, and the family lived happily ever afterward.

> We have further docked this tail into: "And they lived happily ever
after.

> So the poor little cinder maid married the Prince, and in time they
came to be King and Queen, and lived happily ever after.

> He had to prove to her that he was not any other woman's sweetheart,
and when he proved that they were married, and they lived happily ever
after, which is the proper way to live.

> After no great delay Crimthann mac Ae agreed and arranged that he and
Becfola should fly from Tara, and it was part of their understanding
that they should live happily ever after.

> But when mature, married and discreet people arrange a match between a
boy and a girl, they do it sensibly, with a view to the future, and
the young couple live happily ever afterwards.

> And then, if you please, with an eye gone and a piece of his face blow
away, he came to the conclusion that the world wasn't such a bad place
after all, and he lived happily ever afterwards.

> But as to Fergus Fionnliath, he took to his bed, and he stayed there
for a year and a day suffering from blighted affection, and he would
have died in the bed only that Fionn sent him a special pup, and in a
week that young hound became the Star of Fortune and the very Pulse of
his Heart, so that he got well again, and he also lived happily ever
after.

Ideas
=====

Perhaps create some chapters beginning "Once upon a time" and ending "happily ever after" or "The end.", each with a load of "And then" or "But why".


