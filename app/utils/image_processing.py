import cv2
import numpy as np
import os


class ImageProcessor:
    def resize_image(image,width=None,height=None,scale_factor=None):
        if scale_factor is not None:
            return cv2.resize(image,None,fx=scale_factor,fy=scale_factor,interpolation=cv2.INNER_LINEAR)
    
        if width == None and height ==None:
            return cv2.resize(image,(width,height),interpolation=cv2.INNER_LINEAR)
        
        raise ValueError("Provide either scale_factor or width and height")
    
    
    def crop_image(image,xstart=0,ystart=0,xend=None,yend=None):
        h,w=image.shape[:2]
        xend=xend or w
        yend=yend or h
        return image[ystart:yend,xstart:xend]
    
    def rotate_image(image,angle=90,scale = 1):
        h,w = image.shape[:2]
        center = (w//2,h//2)
        
        rotation_matrix = cv2.getRotationMatrix2D(center,angle,scale)
        
        return cv2.warpAffine(image,rotation_matrix,(w,h))
    
    def add_watermark(image,watermark,position=(10,10),alpha=0.5):
        watermark = ImageProcessor.resize_image(watermark,width=image.shape[1]//4)
        
        roi = image[
            position[1]:position[1]+watermark.shape[0] ,
            position[0]:position[0]+watermark.shape[1]
        ]
        
        blended = cv2.addWeighted(roi,1-alpha,watermark,alpha,0)
        
        image[
            position[1]:position[1]+watermark.shape[0],
            position[0]:position[0]+watermark.shape[1]
        ] = blended
        
        return image
    
    def flip_image(image,mode="horizontal"):
        flip_modes = {
            'horizontal':1,
            'vertical':0,
            'both':-1
        }
        
        if mode not in flip_modes:
            raise ValueError("Mention horizontal flip or vertical flip")
        
        return cv2.flip(image,flip_modes[mode])
    
    def apply_filters(image,filter_type='grayscale'):
        if filter_type == 'grayscale':
            return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        
        elif filter_type == 'sepia':
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168], 
                               [0.393, 0.769, 0.189]])
            
            sepia_image = cv2.transform(image,kernel)
            sepia_image = np.clip(sepia_image,0,255).astype(np.unit8)
            return sepia_image
        elif filter_type == 'negative':
            return 255-image
        
        else:
            raise ValueError("Unsupported filter type")
        
    def compress_image(image,quality=80):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),quality]
        result,encode_img = cv2.imencode('.jpg',image,encode_param)
        
        if not result:
            raise ValueError("Image Compression Failed")
        
        return cv2.imdecode(encode_img,cv2.IMREAD_COLOR)
    
    def change_format(image,output_format='png'):
        formats = {
            'png': cv2.IMWRITE_PNG_COMPRESSION,
            'jpg': cv2.IMWRITE_JPEG_QUALITY,
            'jpeg': cv2.IMWRITE_JPEG_QUALITY
        }
        
        if output_format not in formats:
            raise ValueError("UnSupported format")
        
        result,encoded_img = cv2.imencode(f'.{output_format}',image)
        
        if not result:
            raise ValueError('Format Conversion Failed')
        
        return cv2.imdecode(encoded_img,cv2.IMREAD_COLOR)
    
    
image_process = ImageProcessor()
        
        
        