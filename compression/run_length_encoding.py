import numpy as np


class Rle:
    def __init__(self):
        pass

    def encode_image(self, binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        rle = []
        for row in range(0, len(binary_image)):
            if binary_image[row][0] == 0:
                rle.append('0')
            else:
                rle.append('255')
            c = 1
            for col in range(1, len(binary_image[0])):
                if binary_image[row][col] == binary_image[row][col-1]:
                    c+=1
                else:
                    rle.append(c)
                    c = 1
        return np.array(rle)


    def fill_white(self, image, row, x, col):
        for i in range(0,int(x)):
            if col <256:
                image[row][col] = 255
                col +=1
        return image

    def fill_black(self, image, row, x, col):
        for i in range(0, int(x)):
            if col < 256:
                image[row][col] = 0
                col += 1
        return image

    def fill_image(self, image, row, line):
        flip = 1
        col = 0
        if line[0] == '0':
            for x in line:
                if flip % 2 == 1:
                    image = self.fill_white(image, row, x, col)
                    col += int(x)
                else:
                    image= self.fill_black(image, row, x, col)
                    col += int(x)
                flip += 1

        if line[0] == '255':
            for x in line:
                if flip % 2 == 1:
                    image = self.fill_black(image, row, x, col)
                    col += int(x)
                else:
                    image = self.fill_white(image, row, x, col)
                    col += int(x)
        return image

    def decode_image(self, rle_code, height, width):
        """
        Get original image from the rle_code
        # takes as input:
        # rle_code: the run length code to be decoded
        # Height, width: height and width of the original image
        # returns decoded binary image
        # """
        image = np.zeros((height, width))
        decode = dict()
        row = -1
        for x in rle_code:
            if x == '0' or x == '255':
                row += 1
                decode.setdefault(row, []).append(x)

            else:
                decode.setdefault(row, []).append(x)

        for row in decode.keys():
            line = decode[row]
            image = self.fill_image(image, row, line)
        return image
