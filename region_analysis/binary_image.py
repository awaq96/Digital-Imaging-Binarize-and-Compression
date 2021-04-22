class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""
        freq = {}
        # create keys for dictionary of occurrences,
        for x in range(0, 256):
            freq[x] = 0

        # count frequency of each bits occurrence
        for x in range(len(image)):
            for y in range(len(image[0])):
                freq[image[x][y]] += 1

        # Make list of Histogram
        list_of_values = []
        for i in sorted(freq.keys()):
            list_of_values.append(freq[i])

        return list_of_values


    def find_otsu_threshold(self, hist):
        """analyses a histogram it to find the otsu's threshold assuming that the input hstogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value (otsu's threshold)"""
        total_num_of_pixels = 0
        for x in hist:
            total_num_of_pixels += x
        probabilities = {}
        for x in range(0,255):
            probabilities[x] = hist[x]/total_num_of_pixels

        threshold_dict = {}
        for thresholds in range(0, 255):
            weight1 = 0
            weight2 = 0
            mean1_total = 0
            mean1_vals = 0
            mean2_total = 0
            mean2_vals = 0
            variance1 = 0
            variance2 = 0
            for t in range(0, thresholds):
                weight1 += probabilities[t]
                mean1_vals += hist[t] * t
                mean1_total += hist[t]

            weight1 /= total_num_of_pixels
            if mean1_total > 0:
                mean1 = mean1_vals / mean1_total
                for x in range(0, thresholds):
                    variance1 += ((x - mean1) ** 2) * hist[x]

            if mean1_total > 0:
                variance1 /= mean1_total

            for t in range(thresholds+1, 255):
                weight2 += probabilities[t]
                mean2_vals += hist[t] * t
                mean2_total += hist[t]

            weight2 /= total_num_of_pixels
            if mean2_total > 0:
                mean2 = mean2_vals / mean2_total
                for x in range(thresholds + 1, 255):
                    variance2 += ((x - mean2) ** 2) * hist[x]
            if mean2_total > 0 :
                variance2 /= mean2_total
                within_class_variance = weight1 * variance1 + weight2 * variance2
                threshold_dict[thresholds] = within_class_variance

        return min(threshold_dict.keys(), key=(lambda k: threshold_dict[k]))


    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        take as input
        image: an grey scale image
        returns: a binary image"""
        histogram = self.compute_histogram(image)
        threshold = self.find_otsu_threshold(histogram)

        for x in range(0, len(image)):
            for y in range(0, len(image[0])):
                if image[x][y] < threshold:
                    image[x][y] = 255
                else:
                    image[x][y] = 0
        bin_img = image.copy()

        return bin_img


