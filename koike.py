import argparse
from os import path as osp

from PIL import Image


def split_arrange(N, img, new_size, name):

    w_total, h_total = new_size

    w = int(w_total / N)
    h = int(h_total / N)

    splits_w = [(img.crop((i * w, 0, (i + 1) * w, h_total)), i) for i in range(N)]

    #to sort by even and odd items
    def key1(item): return item[1] % 2 == 0

    # #split and arrange width wise
    arranged_w = sorted(splits_w, key=key1)

    new_im = Image.new("RGB", new_size)

    x_offset = 0
    for i, item in enumerate(arranged_w):
        im = item[0]
        if i == 0:
            im = im.rotate(180)

        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    img = new_im
    new_im.show()


    #split and arrange height wise
    splits_h = [(img.crop((0, i * h, w_total, (i + 1) * h)), i) for i in range(N)]
    arranged_h = sorted(splits_h, key=key1)

    img = img.rotate(90)
    
    new_im = Image.new("RGB", (new_size))
    new_im = new_im.rotate(90)

    y_offset = 0
    for i, item in enumerate(arranged_h):
        im = item[0]
        if i == 0:
            im = im.rotate(180)

        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]

    new_im.show()
    new_im.save(f"output-{name}")


def fix_N(n: int, w: int, h: int):
    return n, n * (w//n), n * (h//n)


def main(N, path):

    with Image.open(path) as img:
        img.show()
        w, h = img.size
        N, new_w,  new_h = fix_N(N, w, h)
        w_diff, h_diff = w - new_w, h - new_h

        # crop img half of w_diff and h_diff in both directions (to fit N)
        img = img.crop((w_diff//2, h_diff//2, w_diff //
                       2 + new_w, h_diff//2 + new_h))

        #do the thing
        split_arrange(N, img, (new_w, new_h), osp.basename(path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("N", help="The number of splits you want to make (width-wise)",
                        nargs="?", type=int, default=64)
    parser.add_argument("path", help= "The filename + extension of your input image located in this folder (e.g 'monkey.jpg')",
                        nargs ="?", type=str, default="monkey.jpg")
    args = parser.parse_args()
    
    main(args.N, args.path)

