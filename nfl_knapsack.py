import csv
import argparse

arg_p = argparse.ArgumentParser()
arg_p.add_argument('-csv', default='')
args = vars(arg_p.parse_args())

CSV = 'wk12.csv'

class Player():
    def __init__(self, position, name, salary, points, value):
        self.self = self
        self.position = position
        self.name = name
        self.salary = salary
        self.points = points
        self.value = value
        
    def __iter__(self):
        return iter(self.list)
    
    def __str__(self):
        return "{} {} {} {}".format(self.name,self.position,self.salary, self.points)

with open(CSV,'r') as data:
    reader = csv.reader(data)
    next(reader)
    players = []
    for row in reader:
        name = row[0]
        position = row[1]
        salary = int(row[2])
        points = float(row[3])
        value = points / salary  
        player = Player(position, name, salary, points, value)
        players.append(player)

def lineup_knapsack(players):
    cap = 50000
    current_lineup_cap = 0
    limits = {
        'QB':1,
        'RB':1,
        'WR':1,
        'TE':1,
        'FLEX':1,
        'DST':1
        }
    
    counter = {
        'QB':0,
        'RB':0,
        'WR':0,
        'TE':0,
        'FLEX':0,
        'DST':0
        }
    
    players.sort(key=lambda x: x.value, reverse=True)
    lineup = []
    
    for player in players:
        nam = player.name
        pos = player.position
        sal = player.salary
        pts = player.points
        if counter['QB'] < limits['QB'] and current_lineup_cap + sal <= cap and pos in ['QB']:
            lineup.append(player)
            counter['QB'] = counter['QB'] + 1
            current_lineup_cap += sal
            continue
        if counter['RB'] < limits['RB'] and current_lineup_cap + sal <= cap and pos in ['RB','FLEX']:
            lineup.append(player)
            counter['RB'] = counter['RB'] + 1
            current_lineup_cap += sal
            continue
        if counter['WR'] < limits['WR'] and current_lineup_cap + sal <= cap and pos in ['WR','FLEX']:
            lineup.append(player)
            counter['WR'] = counter['WR'] + 1
            current_lineup_cap += sal
            continue
        if counter['TE'] < limits['TE'] and current_lineup_cap + sal <= cap and pos in ['TE','FLEX']:
            lineup.append(player)
            counter['TE'] = counter['TE'] + 1
            current_lineup_cap += sal
            continue
        if counter['FLEX'] < limits['FLEX'] and current_lineup_cap + sal <= cap and pos in ['RB','WR']:
            lineup.append(player)
            counter['FLEX'] = counter['FLEX'] + 1
            current_lineup_cap += sal
            continue
        if counter['DST'] < limits['DST'] and current_lineup_cap + sal <= cap and pos in ['DST']:
            lineup.append(player)
            counter['DST'] = counter['DST'] + 1
            current_lineup_cap += sal 
    
    players.sort(key=lambda x: x.points, reverse=True)
    for player in players:
        nam = player.name
        pos = player.position
        sal = player.salary
        pts = player.points
        if player not in lineup:
            pos_players = [ x for x in lineup if x.position == pos]
            pos_players.sort(key=lambda x: x.points)
            for pos_player in pos_players:
                if (current_lineup_cap + sal - pos_player.salary) <= cap and pts > pos_player.points:
                    lineup[lineup.index(pos_player)] = player
                    current_lineup_cap = current_lineup_cap + sal - pos_player.salary
                    break
    return lineup

lineup = lineup_knapsack(players)
points = 0
salary = 0
for player in lineup:
    points += player.points
    salary += player.salary
    print(player)
print("\nPoints: {}".format(points))
print("Salary: {}".format(salary))