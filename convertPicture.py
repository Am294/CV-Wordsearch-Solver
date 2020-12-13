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
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 26)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        x = self.dropout1(x)
        output = F.log_softmax(x, dim=1)
        return output

def predict_photo(img, model):
    model.eval()
    output = model(img[None, ...].float())
    pred = output.argmax(dim=1, keepdim=True)

    
    return chr(pred.item() + 65)

def grid_to_letters(img_path, is_ws):
    MIN_CONTOUR_AREA = 10   
    img = cv2.imread(img_path) 
    img_copy = img.copy()
    dim = (img.shape[1] , img.shape[0]) 
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    model = Net()
    model.load_state_dict(torch.load('model/letterModel.dat', map_location='cpu'))
    transform=torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.1307,), (0.3081,))
        ])
    
    #dst = cv2.Canny(gray, 0, MIN_CONTOUR_AREA)   
    #blured = cv2.blur(dst, (5,5), 0)    
    img_thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    Contours, Hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    count = 0
    word_search = []
    final_word_search = []
    current_row = []
    prev_y = -1
    prev_x = -1
    for contour in Contours:
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
            [X, Y, W, H] = cv2.boundingRect(contour)
            print(X,Y)
            cv2.rectangle(img, (X, Y), (X + W, Y + H), (0,0,255), 2)
            roi = gray[Y-2:Y+H+2,X-2:X+W+2]
            roi = cv2.bitwise_not(roi)
            #cv2.imwrite(f'images/output/w{count}.PNG', roi)
            roi_re = cv2.resize(roi,(28,28))
            roi_torch = transform(roi_re)
            #cv2.imwrite(f'images/output/t{count}.PNG', roi_re)
                

            if is_ws:    
                if prev_y != -1 and abs(prev_y - Y) > 10:
                    word_search.append(current_row[::-1])
                    current_row = []
            
            else:
                if (prev_y != -1 and prev_x != -1) and (abs(prev_y - Y) > 10) or (abs(prev_x - X) > 25):
                    word = ''.join(current_row[::-1])
                    if word != '':
                        word_search.append(word)
                        current_row = []
            
            letter = predict_photo(roi_torch, model)
            prev_y = Y
            prev_x = X
            current_row.append(letter)

            count += 1

    
    if is_ws:
        word_search.append(current_row[::-1])
        for w in reversed(word_search):
            final_word_search.append(w)
    else:
        word = ''.join(current_row[::-1])
        word_search.append(word)
        final_word_search = sorted(word_search)

    cv2.imwrite("images/output/full.PNG", img)

    return final_word_search
            
        
