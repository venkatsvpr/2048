from random import randint
from BaseAI import BaseAI
from Displayer  import Displayer
from Grid import Grid
from copy import deepcopy
from sets import Set
from ComputerAI import ComputerAI

defaultProbability = 0.9
AllowedDepth = 3

depth = 0
depth_min = False
depth_max= False
pow2 ={1:0, 2:1, 4:2 , 8:3, 16:4, 32:5, 64:6, 128:7, 256:8, 512:9, 1024:10, 2048:11}
class PlayerAI(BaseAI):

    def getMove(self, grid):

        disp = Displayer()
        #print " display grid"
        #disp.display(grid)
        tgrid = Grid()
        tempgrid = Grid ()
        tgrid.map = deepcopy(grid.map)
        tgrid.size = grid.size

        tempgrid.map = deepcopy(grid.map)
        tempgrid.size = grid.size

        #print "grid"
        #disp.display(grid)
        tChild,tUtil = self.decision(grid)

        #print " before move tgrid"
        #disp.display(tgrid)
        #tgrid.move(0)
        #print "tgrid"
        #disp.display(tgrid)
        #print "grid"
        #disp.display(grid)
        #if (tgrid == grid):
        #    return 0

        #tgrid.map = deepcopy(tempgrid.map)
        #tgrid.size = tempgrid.size

        dir = 0
        while(dir <4):
            tgrid.move(dir)
            #print "tgrid"
            #disp.display(tgrid)
            #print "grid"
            #disp.display(grid)
            if (self.is_equal(tgrid,grid)):
                if (not tempgrid.move(dir)):
                    count = 4
                    while(count):
                        dir  = (dir + 1) % 4
                        if (tempgrid.move(dir)):
                            return dir
                        count -= 1
                else:
                    return dir
            tgrid.map = deepcopy(tempgrid.map)
            tgrid.size = tempgrid.size
            dir += 1    

        """print "grid"
        disp.display(grid)
        return rand(0,2)    """
        #print " \n"
        #print "grid"
        #disp.display(grid)
        #print "tgrid"
        #disp.display(tgrid)
        #print "up"
        #print tUtil
        #print "No Moves"

    def decision(self,grid):
        global depth
        depth = 0
        alpha = -999999
        beta  = 999999
        #print "dec",depth
        return self.maximize(grid,alpha,beta)
        
    def maximize(self,grid,alpha,beta):
        global depth,depth_max
        #print "max ",depth,"alpha",alpha,"beta",beta
        disp = Displayer()
      
        depth += 1
        maxChild = None
        maxUtil = -999999

        if (self.is_grid_terminal(grid)):
            #print "terminal max"
            return None,self.eval(grid)

        if (depth>=AllowedDepth):
            #print "depth max",self.eval(grid),depth
            depth_max=True
            return None,self.eval(grid)
        
        moves = grid.getAvailableMoves()
        best_move = 4
        for move in moves:
            tgrid = Grid()
            tgrid.map = deepcopy(grid.map)
            tgrid.size = grid.size
            #print "tgrid",move
            #disp.display(tgrid)
            tgrid.move(move)
            #disp.display(tgrid)
         
            tChild,tUtil = self.minimize(tgrid,alpha,beta)
            depth = depth-1

            if(tUtil > maxUtil):
                best_move = move
                maxUtil= tUtil

            if maxUtil >=alpha:
                alpha = maxUtil

            if (alpha >= beta):
                #print "break maxutil",maxUtil,"beta",beta
                break

            """"if (depth_min):
                print "depth min set"
                disp.display(grid)"""
        if (best_move <4):
            maxChild = grid.move(best_move)

        return maxChild,maxUtil

    def minimize(self,grid,alpha,beta):
      
        global depth,depth_min
        #print "mini ",depth,"alpha",alpha,"beta",beta
        depth +=1
        if (self.is_grid_terminal(grid)):
            #print "grid terminal"
            return None,self.eval(grid)

        if (depth>=AllowedDepth):
            depth_min=True
            #print "depth min",self.eval(grid),depth
            return None,self.eval(grid)
        
        minChild = None
        minUtil = +99999
        
        count = 0
        while (count < 1):
            ai = ComputerAI()
            tgrid = Grid()
            tgrid.map = deepcopy(grid.map)
            tgrid.size = grid.size
            cell= ai.getMove(grid)
            title = self.getNewTileValue()
            tgrid.setCellValue(cell, title)

            if (count > 0):
                if (cell == prev_cell) and (prev_title == title):
                    break
                
            tChild,tUtil =  self.maximize(tgrid,alpha,beta);
            depth = depth - 1

            if (minUtil > tUtil):
                minChild = grid.setCellValue(cell, title)
                minUtil = tUtil

            if  minUtil < beta:
                beta = minUtil

            if (alpha >= beta):
                break;

            count = count + 1 
            prev_cell = cell
            prev_title = title
        return (minChild,minUtil)

    def near_by(self,grid,x,y):
        end = grid.size-1
        if grid.map[x][y] == 0:
            return False
        
        if (x != 0):
            #print x-1
            if (grid.map[x][y] == grid.map [x-1][y]):
                #print x,y,"True return"
                return True
        if (x < end):
            if (grid.map [x][y] == grid.map[x-1][y]):
                #print x,y,"True return"
                return True
        if (y != 0):
            if (grid.map[x][y] == grid.map[x][y-1]):
                #print x,y,"True return"
                return True
        if (y<end):
            if (grid.map[x][y] == grid.map[x][y+1]):
                #print x,y,"True return"
                return True
        return False
    def check_zero(self,grid):
        num_zeros = grid.size * grid.size
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                if grid.map[x][y] != 0:
                    num_zeros -= 1
        return num_zeros
    
    def one_direction(self,grid,direction):
        tgrid = Grid()
        tgrid.map = deepcopy(grid.map)
        tgrid.size = grid.size
        tgrid.move(direction)
        tzero = self.check_zero(tgrid)
        gzero = self.check_zero(grid)
        return abs(gzero - tzero)
        
    def hfn(self,grid):
        dis = Displayer()
        escore = 128
        dict_scores ={}
        #dis.display(grid)
        num_zeros =self.check_zero(grid)
        ####Number of zeros
        escore += num_zeros *128


        for x in xrange(grid.size):
            for y in xrange(grid.size):
                if grid.map[x][y] != 0:
                    val = grid.map[x][y]
                    if val in  dict_scores:
                        dict_scores[val] += 1
                    else:
                        dict_scores[val] = 1

        tgrid = Grid()
        tgrid.map = deepcopy(grid.map)
        tgrid.size =grid.size

        ### Degree of freedom
        num_moves = 4
        direction = 3
        while (direction >=0):
            tgrid = Grid()
            tgrid.map = deepcopy(grid.map)
            tgrid.size = grid.size
            if (False == tgrid.move(direction)):
                num_moves -= 1
            direction =-1
        escore += num_moves * 256

        ### values
        for key in dict_scores:
            #print key,dict_scores[key]
            escore += pow2[key] * dict_scores[key]*2

        ### Nearby match
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                if grid.map[x][y] != 0:
                    if(self.near_by(grid,x,y)):
                        escore += 3* grid.map[x][y]

        ### one direction match
        direction = 3
        matches = 0
        while(direction):
            matches+=self.one_direction(grid,direction)
            direction -= 1
        
        escore += matches * 50

        ## types
        escore += 3*(11-len(dict_scores))

        ## diff between max and second max

        diff = 2048 - self.diff_max(grid)
        escore += 3*abs(diff)

        ## if big number in center or corner
        if (self.is_big_in_corner(grid)):
            escore += 5

        ## check if big numbers are in corners or sides
        escore += 5*self.big_four_corner(grid)

        #print escore
        #print "hfn"
        #
        #print escore
        return escore

    def diff_max(self,grid):
        max1 = 0
        max2 = 0
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                if (grid.map[x][y] != 0):
                    if (grid.map[x][y] > max1):
                        max1 = grid.map[x][y]
                    elif (grid.map[x][y] > max2):
                        max2 = grid.map[x][y]
        return abs(max1-max2)

    def find_x_y(self,grid,element):
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                if (grid.map[x][y] == element):
                    return x,y
        
    def big_four_corner(self,grid):
        end = grid.size-1
        max1 = 0
        max2 = 0
        max3 = 0
        max4 = 0
        ret = 0
        m1x = m1y = m2x = m2y = m3x = m3y =m4x = m4y = grid.size
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                if (grid.map[x][y] != 0):
                    if (grid.map[x][y] > max1):
                        max1 = grid.map[x][y]
                        m1x = x
                        m1y = y
                    elif (grid.map[x][y] > max2):
                        max2 = grid.map[x][y]
                        m2x =x
                        m2y= y
                    elif (grid.map[x][y] > max3):
                        max3 = grid.map[x][y]
                        m3x = x
                        m3y = y
                    elif (grid.map[x][y] > max4):
                        max4 = grid.map[x][y]
                        m4x = x
                        m4y = y


        if (max1 >0 and max2 > 0):       
            if (m1x == m2x) or (m1y == m2y):
                ret += 5
        if (max3 >0 and max4 >0):
            if (m3x * m3y *m4x *m4y != 0):
                if (m3x == m4x) or (m3y == m4y):
                    ret += 2
  
        return ret
    
    def is_big_in_corner(self,grid):
        max1 = 0
        x_pos = 0
        y_pos = 0
        end = grid.size-1
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                if (grid.map[x][y] != 0):
                    if (grid.map[x][y] > max1):
                        max1 = grid.map[x][y]
                        x_pos =x
                        y_pos = y
        if(x_pos == y_pos) or (x_pos == 0 and y_pos == end) or (x_pos==end and y_pos ==0):
            return True
        
    
    def eval(self,grid):
        if (self.is_grid_terminal(grid)):
            return 100000
        else:
            return self.hfn(grid)
        

    def is_grid_terminal(self,grid):
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                if grid.map[x][y] == 2048:
                    return True
        return False

    def getNewTileValue(self):
        possibleNewTiles = [2, 4]
        if randint(0,99) < 100 * defaultProbability:
            return possibleNewTiles[0]
        else:
            return possibleNewTiles[1];

    def is_equal(self,grid1,grid2):
        if(grid1.size != grid2.size):
            return False
        
        for x in xrange(grid1.size):
            for y in xrange(grid1.size):
                if grid1.map[x][y] != grid2.map[x][y]:
                    #print "Not Equal"
                    return False
        #print "Equal" 
        return True       
