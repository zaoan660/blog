import cv2
import numpy as np
import time

def resize(src, width,height):
    dst_w =  width
    dst_h = height
    src_h, src_w = src.shape[:2]
    if src_h == dst_h and src_w == dst_w:
        return src.copy()
    scale_x = float(src_w) / dst_w
    scale_y = float(src_h) / dst_h
    dst = np.zeros((dst_h, dst_w, 3), dtype=np.uint8)
    np_src_x = np.arange(0, dst.shape[1])
    np_src_y = np.arange(0, dst.shape[0]).reshape((dst.shape[0], 1))
    src_x = (np_src_x + np.zeros(dst.shape[:2]))[:, :, np.newaxis] + np.zeros(dst.shape)
    src_y = (np_src_y + np.zeros(dst.shape[:2]))[:, :, np.newaxis] + np.zeros(dst.shape)
    src_x_dst = src_x * scale_x
    src_y_dst = src_y * scale_y
    srcX0 = np.floor(src_x_dst).astype(int)
    srcY0 = np.floor(src_y_dst).astype(int)
    srcX1 = np.minimum(srcX0 + 1, src_w - 1)
    srcY1 = np.minimum(srcY0 + 1, src_h - 1)
    three_axis = np.zeros(dst.shape, dtype=int)
    three_axis[:, :, 1] = 1
    three_axis[:, :, 2] = 2
    value0 = (srcX1 - src_x_dst) * src[srcY0, srcX0, three_axis] + (src_x_dst - srcX0) * src[srcY0, srcX1, three_axis]
    value1 = (srcX1 - src_x_dst) * src[srcY1, srcX0, three_axis] + (src_x_dst - srcX0) * src[srcY1, srcX1, three_axis]
    dst = ((srcY1 - src_y_dst) * value0 + (src_y_dst - srcY0) * value1).astype(np.uint8)
    return dst

img_in = cv2.imread('./lena.jpg')
start = time.time()
img_out = cv2.resize(img_in, (1024,1024))
end = time.time()
print ('cost %f seconds' % (end- start))
img2=resize(img_in,1024,1024)
print('cost %f seconds' % (time.time() - end))
cv2.imshow('src_image', img_in)
cv2.imshow('cv2_image', img_out)
cv2.imshow('customize_imge',img2)
cv2.waitKey()