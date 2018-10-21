
# coding: utf-8

# In[ ]:
import sys

import numpy as np
import cv2
from matplotlib import pyplot as plt
import skin_detector

input_url = sys.argv[1]
print(input_url)
output_url = sys.argv[2]
image = cv2.imread(input_url)
mask = skin_detector.process(image)
mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
mask = cv2.bitwise_not(mask)
mask = cv2.bitwise_not(mask)
result = mask*image
result = cv2.bitwise_not(result)
dst = cv2.fastNlMeansDenoisingColored(result, h=5)
cv2.imwrite(output_url, dst)

