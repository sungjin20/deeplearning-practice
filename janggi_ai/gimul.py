'''
기물 별 이동 가능 위치를 출력하는 함수를 만듦
'''

name_dic={'none':0, 'tank':1, 'horse':2, 'elephant':3, 'mortar':6, 'greenery':7, 'seonbi':4, 'king':5}
s=[[0 for i in range(11)] for j in range(10)]  # current board's stat = s
#output=[]  # return of this module

class type:
    def team(self, input):
        self.team=input
    
    def type(self, input):
        self.type=input%10
        
def tank(x, y): # return tank's possible coordinates    
    output=[]
    start=x
    last=x
    for i in range(x, 0, -1): # x coordinate check
        if s[i][y].type==0:
            start=i
        else:
            if s[i][y].team!=s[x][y].team:
                start=i
                break
            elif i!=x:
                break
                
    for i in range(x, 10):
        if s[i][y].type==0:
            last=i
        else:
            if s[i][y].team!=s[x][y].team:
                last=i
                break
            elif i!=x:
                break 
                
    for i in range(start, last+1): # possible x coordinate append
        if i!=x:
            output.append((i, y))
    
    start=y
    last=y
    for i in range(y, 0, -1): # x coordinate check
        if s[x][i].type==0:
            start=i
        else:
            if s[x][i].team!=s[x][y].team:
                start=i 
                break
            elif i!=y:
                break
                
    for i in range(y, 11):
        if s[x][i].type==0:
            last=i
        else:
            if s[x][i].team!=s[x][y].team:
                last=i 
                break
            elif i!=y:
                break 
                    	
    for i in range(start, last+1):
        if i!=y:
            output.append((x, i))
            
    possible_coordinate=[[(4, 1), (5, 2) ,(6, 3)], [(4, 3), (5, 2), (6, 1)], [(4, 10), (5, 9), (6, 8)], [(4, 8), (5, 9), (6, 10)]]
    for i in possible_coordinate:
        if (x, y) in i:
            for j in i:
                if (x, y)!=j:
                    output.append(j)
        
    return output
    
def horse(x, y):  # return horse's possible coordinates
    output=[]
    if x+1<9 and s[x+1][y].type==0:
        if (y+1<=10 and (s[x+2][y+1].type==0 or s[x][y].team!=s[x+2][y+1].team)):
             output.append((x+2, y+1))
        if (y-1>0 and (s[x+2][y-1].type==0 or s[x][y].team!=s[x+2][y-1].team)):
            output.append((x+2, y-1))
    
    if x-1>1 and s[x-1][y].type==0:
        if (y+1<=10 and (s[x-2][y+1].type==0 or s[x][y].team!=s[x-2][y+1].team)):
             output.append((x-2, y+1))
        if (y-1>0 and (s[x-2][y-1].type==0 or s[x][y].team!=s[x-2][y-1].team)):
            output.append((x-2, y-1))
    
    if y+1<10 and s[x][y+1].type==0:
        if (x+1<=9 and (s[x+1][y+2].type==0 or s[x][y].team!=s[x+1][y+2].team)):
             output.append((x+1, y+2))
        if (x-1>0 and (s[x-1][y+2].type==0 or s[x][y].team!=s[x-1][y+2].team)):
            output.append((x-1, y+2))
            
    if y-1>1 and s[x][y-1].type==0:
        if (x+1<=9 and (s[x+1][y-2].type==0 or s[x][y].team!=s[x+1][y-2].team)):
             output.append((x+1, y-2))
        if (x-1>0 and (s[x-1][y-2].type==0 or s[x][y].team!=s[x-1][y-2].team)):
            output.append((x-1, y-2))
    return output

def elephant(x, y):  # return elephant's possible coordinates
    output=[]
    if x+2<9 and s[x+1][y].type==0:
        if y+1<10 and s[x+2][y+1].type==0 and (s[x+3][y+2].type==0 or s[x+3][y+2].team!=s[x][y].team):
             output.append((x+3, y+2))
        if y-1>1 and s[x+2][y-1].type==0 and (s[x+3][y-2].type==0 or s[x+3][y-2].team!=s[x][y].team):
             output.append((x+3, y-2))
             
    if x-2>1 and s[x-1][y].type==0:
        if y+1<10 and s[x-2][y+1].type==0 and (s[x-3][y+2].type==0 or s[x-3][y+2].team!=s[x][y].team):
             output.append((x-3, y+2))
        if y-1>1 and s[x-2][y-1].type==0 and (s[x-3][y-2].type==0 or s[x-3][y-2].team!=s[x][y].team):
             output.append((x-3, y-2))
             
    if y+2<10 and s[x][y+1].type==0:
        if x+1<9 and s[x+1][y+2].type==0 and (s[x+2][y+3].type==0 or s[x+2][y+3].team!=s[x][y].team):
             output.append((x+2, y+3))
        if x-1>1 and s[x-1][y+2].type==0 and (s[x-2][y+3].type==0 or s[x-2][y+3].team!=s[x][y].team):
             output.append((x-2, y+3))
             
    if y-2>1 and s[x][y-1].type==0:
        if x+1<9 and s[x+1][y-2].type==0 and (s[x+2][y-3].type==0 or s[x+2][y-3].team!=s[x][y].team):
             output.append((x+2, y-3))
        if x-1>1 and s[x-1][y-2].type==0 and (s[x-2][y-3].type==0 or s[x-2][y-3].team!=s[x][y].team):
             output.append((x-2, y-3))
             
    return output
    
def mortar(x, y):  # return mortar's possible coordinates
    output=[]
    
    first=0  # x coordinate check
    second=0
    for i in range(1, x):
         if s[i][y].type!=0 and i!=x:
             second=first
             first=i
             
    if first!=0:
        if second!=0:
            if s[second][y].type!=name_dic['mortar']:
                if s[first][y].type!=name_dic['mortar'] and s[first][y].team!=s[x][y].team:
                    output.append((first, y))
                for i in range(first+1, second):
                    output.append((i, y))
        else:
            if s[first][y].type!=name_dic['mortar']:
                for i in range(1, first):
                    output.append((i, y))
    
    first=0
    second=0
    for i in range(x+1, 10):
         if s[i][y].type!=0:
             second=first
             first=i
         if second!=0:
             break
    
    if first!=0:
        if second!=0:
            if s[first][y].type!=name_dic['mortar']:
                if s[second][y].type!=name_dic['mortar'] and s[first][y].team!=s[x][y].team:
                    output.append((second, y))
                for i in range(first+1, second):
                    output.append((i, y))
        else:
            if s[first][y].type!=name_dic['mortar']:
                for i in range(first+1, 10):
                    output.append((i, y))
            
    first=0  # y coordinate check
    second=0
    for i in range(1, y):
         if s[x][i].type!=0 and i!=y:
             second=first
             first=i
             
    if first!=0:
        if second!=0:
            if s[x][second].type!=name_dic['mortar']:
                if s[x][first].type!=name_dic['mortar'] and s[x][first].team!=s[x][y].team:
                    output.append((x, first))
                for i in range(first+1, second):
                    output.append((x, i))
        else:
            if s[x][first].type!=name_dic['mortar']:
                for i in range(1, first):
                    output.append((x, i))
    
    first=0
    second=0
    for i in range(y+1, 11):
         if s[x][i].type!=0:
             second=first
             first=i
         if second!=0:
             break
    
    if first!=0:
        if second!=0:
            if s[x][first].type!=name_dic['mortar']:
                if s[x][second].type!=name_dic['mortar'] and s[x][first].team!=s[x][y].team:
                    output.append((x, second))
                for i in range(first+1, second):
                    output.append((x, i))
        else:
            if s[x][first].type!=name_dic['mortar']:
                for i in range(first+1, 11):
                    output.append((x, i))
    
    if x==4 and y==1 and s[5][2].type!=0 and s[5][2].type!=name_dic['mortar'] and s[6][3].team!=s[4][1].team:
        output.append((6, 3))
        
    if x==6 and y==1 and s[5][2].type!=0 and s[5][2].type!=name_dic['mortar'] and s[4][3].team!=s[6][1].team:
        output.append((4, 3))
        
    if x==4 and y==3 and s[5][2].type!=0 and s[5][2].type!=name_dic['mortar'] and s[6][1].team!=s[4][3].team:
        output.append((6, 1))
            
    if x==6 and y==1 and s[5][2].type!=0 and s[5][2].type!=name_dic['mortar'] and s[4][3].team!=s[6][1].team:
        output.append((4, 3))
            
    if x==4 and y==10 and s[5][2].type!=0 and s[5][9].type!=name_dic['mortar'] and s[6][8].team!=s[4][10].team:
        output.append((6, 8))
            
    if x==6 and y==10 and s[5][2].type!=0 and s[5][9].type!=name_dic['mortar'] and s[4][8].team!=s[6][10].team:
        output.append((4, 8))
            
    if x==4 and y==8 and s[5][2].type!=0 and s[5][9].type!=name_dic['mortar'] and s[6][10].team!=s[4][8].team:
        output.append((6, 10))
            
    if x==6 and y==8 and s[5][2].type!=0 and s[5][9].type!=name_dic['mortar'] and s[4][10].team!=s[6][8].team:
        output.append((4, 10))
       
    return output

def greenery(x, y):
    output=[]
    possible_coordinate={(4, 3) : [(5, 2)], (6, 3) : [(5, 2)], (5, 2) :  [(4, 1), (6, 1)], (4, 8) : [(5, 9)], (6, 8) : [(5, 9)], (5, 9) : [(4,10), (6, 10)]}
    if s[x][y].team==2:
        if x-1>0 and (s[x-1][y].team!=s[x][y].team or s[x-1][y].type==0):
            output.append((x-1, y))
        if x<9 and (s[x+1][y].team!=s[x][y].team or s[x+1][y].type==0):
            output.append((x+1, y))
        if y-1>0 and (s[x][y-1].team!=s[x][y].team or s[x][y-1].type==0):
            output.append((x, y-1))
    else:        
        if x-1>0 and (s[x-1][y].team!=s[x][y].team or s[x-1][y].type==0):
            output.append((x-1, y))
        if x<9 and (s[x+1][y].team!=s[x][y].team or s[x+1][y].type==0):
            output.append((x+1, y))
        if y<10 and (s[x][y+1].team!=s[x][y].team or s[x][y+1].type==0):
            output.append((x, y+1))
            
    if (x, y) in possible_coordinate.keys():
            for i in possible_coordinate[(x, y)]:
                output.append(i)
            
    return output
    
def seonbi(x, y):
    output=[]
    possible_coordinate={(4, 3) : [(5, 2), (4, 2), (5, 3)], (5, 3) : [(5, 2), (6, 3), (4, 3)], (6, 3) :  [(5, 3), (5, 2), (6, 2)],(4, 2) : [(5, 3), (4, 1), (5, 2)], (5, 2) : [(4, 1), (4, 2), (4, 3), (5, 1), (5, 3), (6, 1), (6, 2), (6, 3)], (6, 2) :  [(5, 2), (6, 1), (6, 3)],(4, 1) : [(5, 2), (4, 2), (5, 1)], (5, 1) : [(5, 2), (6, 1), (4, 1)], (6, 1) :  [(5, 1), (5, 2), (6, 2)],(4, 8) : [(4, 10), (5, 8), (5, 9)], (5, 8) : [(4, 8), (6, 8), (5, 9)], (6, 8) : [(5, 8), (5, 9), (6, 9)],(4, 9) : [(4, 8), (4, 10), (5, 9)], (5, 9) : [(4, 8), (4, 9), (4, 10),(5,8), (5, 10), (6, 8), (6, 9), (6, 10)], (6, 9) : [(6, 8), (6, 10), (5, 9)],(4, 10) : [(4, 9), (5, 9), (5, 10)], (5, 10) : [(4, 10), (6, 10), (5, 9)], (6, 10) : [(5, 9), (6, 9), (5, 10)]}
     
    for i in possible_coordinate[(x, y)]:
        if s[i[0]][i[1]].team!=s[x][y].team or s[i[0]][i[1]].type==0:
            output.append(i)
            
    return output
    
def gimul_coordinate(x, y, stat):
    
    if not(0<x<10) or not(0<y<11):  # wrong coordinate input check
        print("wrong coordinate input")
        return -1;
    
    for i in range(1, 10):  # reset input to class
        for j in range(1, 11):
            s[i][j]=type()
            if stat[i][j]>10:
                s[i][j].team(2)
            elif stat[i][j]!=0: 
                s[i][j].team(1)
            else:
                s[i][j].team(0)
            s[i][j].type(stat[i][j]%10)
            
    	        
    if s[x][y].type==name_dic['tank']: # return possible coordinates by type
        return tank(x, y)
    elif s[x][y].type==name_dic['horse']:
        return horse(x, y)
    elif s[x][y].type==name_dic['elephant']:
        return elephant(x, y)
    elif s[x][y].type==name_dic['mortar']:
        return mortar(x, y)
    elif s[x][y].type==name_dic['greenery']:
        return greenery(x, y)
    elif (s[x][y].type==name_dic['seonbi'] or s[x][y].type==name_dic['king']):
        return seonbi(x, y)
    elif s[x][y].type==name_dic['none']:
        print("no gimul is at (%d, %d)", x, y)
        return -1
    else:
        print("gimul type error")
        return -1
        