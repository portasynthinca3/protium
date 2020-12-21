"""
thanks to:
https://stackoverflow.com/a/63639583/8074626
"""

from PIL import ImageDraw, Image

class ExtendedImageDraw(ImageDraw.ImageDraw):

    def rounded_rectangle(self, xy, corner_radius, fill=None, outline=None):
        upper_left_point = xy[0]
        bottom_right_point = xy[1]

        if fill is None:
            raise ValueError('fill is None')

        if outline is None:
            outline = fill

        self.pieslice([upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)],
            180,
            270,
            fill=fill,
            outline=outline
        )
        self.pieslice([(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point],
            0,
            90,
            fill=fill,
            outline=outline
        )
        self.pieslice([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2), (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],
            90,
            180,
            fill=fill,
            outline=outline
        )
        self.pieslice([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]), (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)],
            270,
            360,
            fill=fill,
            outline=outline
        )
        self.rectangle(
            [
                (upper_left_point[0], upper_left_point[1] + corner_radius),
                (bottom_right_point[0], bottom_right_point[1] - corner_radius)
            ],
            fill=fill,
            outline=fill
        )
        self.rectangle(
            [
                (upper_left_point[0] + corner_radius, upper_left_point[1]),
                (bottom_right_point[0] - corner_radius, bottom_right_point[1])
            ],
            fill=fill,
            outline=fill
        )
        self.line([(upper_left_point[0] + corner_radius, upper_left_point[1]), (bottom_right_point[0] - corner_radius, upper_left_point[1])], fill=outline)
        self.line([(upper_left_point[0] + corner_radius, bottom_right_point[1]), (bottom_right_point[0] - corner_radius, bottom_right_point[1])], fill=outline)
        self.line([(upper_left_point[0], upper_left_point[1] + corner_radius), (upper_left_point[0], bottom_right_point[1] - corner_radius)], fill=outline)
        self.line([(bottom_right_point[0], upper_left_point[1] + corner_radius), (bottom_right_point[0], bottom_right_point[1] - corner_radius)], fill=outline)
    
    def circled_image(self, size: tuple, img: Image.Image):
        ext_size = (size[0] * 4, size[1] * 4)
        mask   = Image.new('L', ext_size)
        mask_d = ExtendedImageDraw(mask)
        mask_d.ellipse((0, 0) + ext_size, fill=255)
        mask   = mask.resize(size, Image.ANTIALIAS)

        img = img.resize(size, Image.BILINEAR)
        img.putalpha(mask)

        return img