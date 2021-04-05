# Ducky Builder!
This directory contains all the assets you need to build a ducky or a man-ducky!


### Templates
In the `templates` folder (`ducky/templates`, `ducky-person/templates`), you'll find the duck components rendered in a silvery gradient. These will be the templates we will paint with random colors to create ducks of random colors. We will simply overlay a transparent color block of the same size to make it look like it's purple or pink or whatever we want.

These assets are the same size, so you simply put them all in the same space and respect transparency.

The layer order must follow the numbers in the filenames - 1 must be on top, and 5 at the very bottom.


### Accessories
In the `accessories` folder (`ducky/accessories`, `ducky-person/accessories`), you'll find hats, equipment, and outfits. These can be overlaid over the duck itself, and have already been positioned and masked to fit perfectly.

Some accessories will overlap one another, so you won't be able to use multiple accessories of any type, but it's usually safe to combine one of each type. For example, one hat and one piece of equipment are always safe. One piece of equipment and one outfit is usually safe. Outfits and hats may clash. Multiple of the same type will never work.


### Ducky
Here's everything you need to render a procedural, random ducky.

### Man Ducky
Here's everything you need to render a procedural, random man-ducky.

There are two variations. These variations have completely different outfits, clothes, and equipment, but they share the same head and hats.

##### Render order, bottom to top:
1. bill
2. head
3. eye
4. clothes, like shirt, pants, and dress
5. outfits (NOT BEARD)
6. equipment, like weapons and wands
7. hands and arms
8. beard (must be rendered on top of everything.)
9. hat


_NEVER RENDER NINJA TOGETHER WITH OTHER ACCESSORIES!_
