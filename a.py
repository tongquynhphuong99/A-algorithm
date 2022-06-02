

import convertJSON as cj
import heapq as heap
import time


def aStar(source, destination):
    # danh sach nut da tham nhung chua kham pha, danh sach chua cac nguoi hang xom
    open_list = {}
    # danh sach nut da tham va da duoc kham pha, nhung nguoi hang xom cua cac nut nay dc dua vao open_list
    closed_list = {}
    
    

    # gia tri chi phi tu nut nguon den nut hien tai
    g_values = {}
    # lay ID nut nguon va nut dich
    sourceID = cj.getOSMId(source[0], source[1])
    destID = cj.getOSMId(destination[0], destination[1])
    
    g_values[sourceID] = 0
    # tinh heuristic cua nut nguon
    h_source = cj.calculateHeuristic(source, destination)
    
    # open list chua chi phi va ID nut
    # them nut nguon vao open_list
    open_list[sourceID]= h_source
    
    t = time.time()
    while(len(open_list) > 0):
        # sap xep open_list theo gia tri nho den lon
       
        s = sorted(open_list.items(), key=lambda x: x[1], reverse=False)
        open_list = {k: v for k, v in s}
        # lay ra gia tri nho nhat 
        curr_state = list(open_list.keys())[0]
        # xoa phan tu nho nhat khoi open list
        if(curr_state == destID):
            print("We have reached to the goal")
            break
       
        del open_list[curr_state]
        #print(curr_state)

        
        # tim cac hang xom cua nut hien tai
        # tra ve thong tin cac hang xom cua nut co ID la Curr_state
        # thong tin bao gom: 
        # key: ID cua hang xom
        # value: toa do, chi phi tu nut hien tai den hang xom, chi phi heuristic tu nut hang xom den dich
        nbrs = cj.getNeighbours(curr_state, destination)
        
        # tra ve thong tin cac hang xom cua nut hien tai
        values = nbrs[curr_state]
        # voi moi nguoi hang xom cua nut hien tai
        for eachNeighbour in values: 
            # eachNeighnour gom ID, toa do, cost, heuristic
        
            neighbourId, neighbourHeuristic, neighbourCost, neighbourLatLon = cj.getNeighbourInfo(
                eachNeighbour)
            
            # g_neighbour = g_current +w(curr, neigh)
            current_inherited_cost = g_values[curr_state] + neighbourCost
            if(curr_state == destID):
                print("We have reached to the goal")
                break
            elif(neighbourId in open_list):
                if (g_values[neighbourId] <= current_inherited_cost):
                    continue
            elif(neighbourLatLon in closed_list):
                if (g_values[neighbourId] <= current_inherited_cost):
                    continue
                # di chuyen nut hang xom tu close sang open
                # open_list.append((neighbourId, g_values[neighbourId]))
                open_list[neighbourId]= neighbourHeuristic
                del closed_list[neighbourLatLon]
            else:
                open_list[neighbourId] = neighbourHeuristic
            # dat g(neighbour)=current_cost
            g_values[neighbourId] = current_inherited_cost
            closed_list[str(neighbourLatLon)] = {"parent": str(
                cj.getLatLon(curr_state)), "cost": neighbourCost}
            
   
    if(len(open_list) == 0):
        print("khong tim dc path")
    print("Time taken to find path(in second): "+str(time.time()-t))
    return closed_list
    
