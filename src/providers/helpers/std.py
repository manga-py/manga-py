
class Std:
    provider = None

    @classmethod
    def _chapters(cls, idx) -> list:
        content = super().get_storage_content()
        return super().document_fromstring(content, idx)

    @classmethod
    def _cover_from_content(cls, selector, img_selector='src') -> str:
        content = super().get_storage_content()
        if content:
            image = super().document_fromstring(content, selector)
            if image and len(image):
                return super().http().normalize_uri(image[0].get(img_selector))

    @classmethod
    def _first_select_options(cls, parser, selector, skip_first=True):
        options = 'option'
        if skip_first:
            options = 'option + option'
        select = parser.cssselect(selector)
        if select:
            return select[0].cssselect(options)
        return []

    @classmethod
    def _images_helper(cls, parser, selector):
        image = parser.cssselect(selector)
        return [i.get('src').strip(r' \r\n') for i in image]

    @classmethod
    def _idx_to_x2(cls, idx, default=0) -> list:
        return [
            idx[0],
            default if len(idx) < 2 or not idx[1] else idx[1]
        ]
