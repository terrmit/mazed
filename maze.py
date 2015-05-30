# coding: utf-8
import random


N = 5
limit = 100
chance = 50




def MakeDownWall(sells, left, right):
  width = right - left
  k = 0
  
  for i in range (left, right + 1):
  
    if random.randint(0, limit) > chance and k < width - 1:
      sells[i]['down'] = True
      k += 1

def MakeLeftWalls(sells, groups):
  
  for i in range (1, N):
    groups[i] = groups[i - 1]
    
    if random.randint(0, limit) > chance:
      sells[i]['left'] = True
      sells[i-1]['right'] = True
      groups[i] += 1

def MakeDownWalls(sells, groups):
  leftSide = 0
  
  for rightSide in range (0, N):
    
    if groups[rightSide] != groups[leftSide] or rightSide == N - 1:
      MakeDownWall(sells, leftSide, rightSide)
      leftSide = rightSide


def MakeMidRow(row):
  groups = []
  
  for i in range (0, N):
    groups.append(1)
        
  MakeLeftWalls(row,groups)
  return groups


def MakeRow(row, rowNumber):
  row[0]['left'] = True
  row[N - 1]['right'] = True
  groups = MakeMidRow(row)

  MakeDownWalls(row,groups)
  
  if rowNumber != N - 1:
    
    if rowNumber == 0:

      for columnNumber in range (0 , N):
        row[columnNumber]['up'] = True
  
  else:
  
    for columnNumber in range (0 , N):
    
      row[columnNumber]['down'] = True


def Generate():
    maze = []

    for i in range(N):
        maze.append([])
  
        for j in range(N):
            maze[i].append({})
            maze[i][j]['up'] = False
            maze[i][j]['down'] = False
            maze[i][j]['left'] = False
            maze[i][j]['right'] = False

    for i in range(N):
        if i != 0:
            for j in range(N):
                maze[i][j]['up'] = maze[i - 1][j]['down']
        MakeRow(maze[i], i)
    
    return maze


Generate()
