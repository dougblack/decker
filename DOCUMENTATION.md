### Documentation

There is a three step process to creating a TTS deck from a decklist.

1. Parse the decklist and retrieve card data and images.
2. Stitch card images into sheet images and upload them to Imgur.
3. Output a TTS-consumable JSON file.

### Card Images

We hit the api.magicthegathering.io to retrieve card data. Example request:

```
GET https://api.magicthegathering.io/v1/cards?name="Wrangle"

{
    "cards": [
        {
            "name": "Wrangle",
            "text": "Gain control of target creature with power 4 or less until end of turn. Untap that creature. It gains haste until end of turn.",
            "imageUrl": "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=423768&type=card"
        }
        ...
    ]
}
```

We then follow the `imageUrl` to get the card face image from
gatherer.wizards.com and cache the response, so we don't have to make
multiple lookups for duplicates.

### Deck Images

TTS expects deck images in single image sheets of 69 cards (and one slot for a
hidden card). Each sheets can hold 7 rows and 10 columns of images. So, we could
represent a 52 card deck in one sheet, but it would take two sheets to make an
80 card deck. The JSON file we load into TTS tells TTS how to slice the sheet
images into individual cards.

In decker, we stitch the cards into groups of 69, produce a sheet image, and upload that
sheet image to Imgur.

### Stacks

A deck has many stacks as well. This represents card stacks that get put into
discrete places in game. A good example is separating the main board and tokens
when loading a new deck into TTS. Each of these would be their own stack.

### JSON

The JSON file tells TTS

1. how to slice the sheet images up to make individual cards
2. the names of individual cards
3. the different card stacks and where to spawn them in-game.
