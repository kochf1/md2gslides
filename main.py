##
## MD2GSlides - Converter between Markdown and Google Slides
## main.py :: main logic
## 
# v0.1 Initial release
#
# Copyright (c) 2025, Dr. Fernando Koch
#    https://github.com/kochf1/md2gslides
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# Disclosure:
# Parts of this code have been generated using GenAI-powered coding tools.
# Human authors have reviewed and adapted the generated code to fit the design intent.
#


import json
from typing import List, Union


class Element:
    def __init__(self, type: str, content: Union[str, List['Element']]):
        self.type = type
        self.content = content

    def __repr__(self):
        return json.dumps({'type': self.type, 'content': self.content}, indent=2)


class Slide:
    def __init__(self):
        self.elements: List[Element] = []

    def add_element(self, element: Element):
        self.elements.append(element)

    def __repr__(self):
        return json.dumps([json.loads(repr(e)) for e in self.elements], indent=2)


class SlideDeck:
    def __init__(self):
        self.slides: List[Slide] = []

    def add_slide(self, slide: Slide):
        self.slides.append(slide)

    def __repr__(self):
        return json.dumps([json.loads(repr(slide)) for slide in self.slides], indent=2)


class Md2Slides:
    def __init__(self, md_filename):
        self.deck = self._load_slides(md_filename)

    @staticmethod
    def _load_slides(filename) -> SlideDeck:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        raw_slides = content.split('---')

        deck = SlideDeck()
        for raw_slide in raw_slides:
            slide_text = raw_slide.strip()
            if slide_text:
                slide = Md2Slides._parse_slide(slide_text)
                deck.add_slide(slide)
        return deck

    @staticmethod
    def _parse_slide(slide_text: str) -> Slide:
        slide = Slide()
        lines = slide_text.splitlines()
        bullet_context = None

        for line in lines:
            line = line.strip()

            if not line:
                bullet_context = None  # End bullet block
                continue

            if line.startswith('#'):
                slide.add_element(Element('title', line))

            elif line.startswith('*'):
                if bullet_context is None:
                    bullet_context = Element('bullets', [])
                    slide.add_element(bullet_context)
                bullet_context.content.append(Element('text', line))

            else:
                slide.add_element(Element('text', line))

        return slide

    def __repr__(self):
        return repr(self.deck)


###
### LAUNCH
###
if __name__ == '__main__':
    md2slides = Md2Slides('slides.md')
    print(md2slides)
