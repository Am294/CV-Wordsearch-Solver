import sys
import numpy as np
import cv2
import torch
import torch.nn.functional as F
import torch.nn as nn
import torchvision

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.conv3 = nn.Conv2d(64, 128, 3, 1)
        self.lin1 = nn.Linear(1152, 128)
        self.lin2 = nn.Linear(128, 26)
        self.avgpool = nn.AvgPool2d(kernel_size=2, stride=2)

    def forward(self, x):
        x = self.conv1(x)
        x = F.tanh(x)
        x = F.max_pool2d(x, 2)
        x = self.conv2(x)
        x = F.tanh(x)
        x = F.max_pool2d(x, 2)
        x = self.conv3(x)
        x = F.tanh(x)
        x = torch.flatten(x, 1)
        x = self.lin1(x)
        x = F.tanh(x)
        x = self.lin2(x)
        return F.log_softmax(x, dim=1)

def predict_photo(img, model):
    model.eval()
    output = model(img[None, ...].float())
    pred = output.argmax(dim=1, keepdim=True)

    
    return chr(pred.item() + 65)

def grid_to_letters(img_path, is_ws):
    MIN_CONTOUR_AREA = 10   
    img = cv2.imread(img_path) 
    img_copy = img.copy()
    if is_ws:
        dim = (img.shape[1] , img.shape[0]*2) 
    else:
        dim = (img.shape[1] , img.shape[0]) 
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    model = Net()
    model.load_state_dict(torch.load('model/letterModel4.dat', map_location='cpu'))
    transform=torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5000,), (0.1500,))
        ])
       
    img_thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    
    Contours, Hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    
    count = 0
    current_grids = []
    grids_arr = []
    final_grids_arr = []
    # Variable for expanding bounding box
    im_es = 2

    prev_y = -1
    prev_x = -1
    
    for contour in Contours:
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
            [X, Y, W, H] = cv2.boundingRect(contour)
            cv2.rectangle(img, (X-im_es, Y-im_es), (X + W + im_es, Y + H + im_es), (0,0,255), 2)
            if is_ws:    
                if prev_y != -1 and abs(prev_y - Y) > 10:
                    current_grids.sort(key=lambda x: (x[0], x[1]))
                    grids_arr.append(current_grids)
                    current_grids = []
            
            else:
                if (prev_y != -1 and prev_x != -1) and (abs(prev_y - Y) > 10) or (abs(prev_x - X) > 45):
                    current_grids.sort(key=lambda x: (x[0], x[1]))
                    grids_arr.append(current_grids)
                    current_grids = []
            


            prev_y = Y
            prev_x = X
        
            if is_ws:
                current_grids.append([X, Y, W, H])
            else:
                current_grids.append([X, Y, W, H])

            count += 1

    if current_grids != []:
        current_grids.sort(key=lambda x: (x[0], x[1]))
        grids_arr.append(current_grids)

    for g in reversed(grids_arr):
        if len(g) > 0:
            final_grids_arr.append(g)
    
    

    final_word_search = []

    i = 0
    for row in final_grids_arr:
        final_word_search.append(['0' for k in row])
        for j in range(len(row)):
            x, y, w, h = row[j][0], row[j][1], row[j][2], row[j][3]
            if is_ws:
                roi = gray[y-6:y+h+6, x-4:x+w+4]
            else:
                roi = gray[y-4:y+h+4, x-3:x+w+3]
            roi = cv2.bitwise_not(roi)
            roi_re = cv2.resize(roi,(28,28))
            if is_ws:
                cv2.imwrite(f'images/output/w{i*25 + j}.PNG', roi_re)
                pass
            roi_torch = transform(roi_re)

            letter = predict_photo(roi_torch, model)
            final_word_search[i][j] = letter
        i += 1

    
   
    cv2.imwrite(f"images/output/bounding{is_ws}.PNG", img)

    return final_word_search, final_grids_arr
    
            
        
