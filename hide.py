#!/usr/bin/env python
# coding: utf-8

# In[6]:


import cv2
import numpy as np
from matplotlib import pyplot as plt
from insightface.app import FaceAnalysis


# In[ ]:


app = FaceAnalysis(name='buffalo_sc', root='./', providers=['CUDAExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))


# In[3]:


img = cv2.imread('images/12.jpeg')
faces = app.get(img)


# In[4]:


bboxes = [face['bbox'] for face in faces]
for e in bboxes:
    img[int(e[1]):int(e[3]), int(e[0]):int(e[2])] = cv2.blur(img[int(e[1]):int(e[3]), int(e[0]):int(e[2])], (50,50))


# In[5]:


plt.imshow(img[:,:,-1])


# In[ ]:




