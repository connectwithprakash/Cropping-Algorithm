import matplotlib.pyplot as plt

from window_method import crop

if __name__ == "__main__":
    file_path = './static/hinton.jpg'
    image = plt.imread(file_path)
    m, n = image.shape[0:-1]
    image = crop(image, center=(m//2+290, n//2), aspect_ratio=(1.4/2.0))
    plt.imsave('./static/output.jpg', image)
    print('Job completed')