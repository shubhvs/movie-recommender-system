#Author : Shubhangi Shimpi
#Assignment3 - CS599
#Program to calculate Pearson Correlation Coefficient and 
#using the values , calculate the predicted ratings 
#Calculates the MAE and RMSE for the CF model



from trainingtest import dataset
from math import sqrt
import csv 
from _operator import concat


#Method to calculate Pearson correlation coefficient 
def pearson_correlation(user1,user2):

    # To get both rated items
    both_rated = {}
    
    for item in dataset[user1]:
        if item in dataset[user2]:
            both_rated[item] = 1

    total_ratings = len(both_rated)        
    
    # Checking for number of ratings in common
    if total_ratings == 0:
        return 0

    
    # Add the ratings of each user
    user1_total_rating = sum([dataset[user1][item] for item in both_rated])
    user2_total_rating = sum([dataset[user2][item] for item in both_rated])
   
    user1_squared_total = sum([pow(dataset[user1][item],2) for item in both_rated])
    user2_squared_total = sum([pow(dataset[user2][item],2) for item in both_rated])

    # sum of product of user1 and user2 ratings for each item
    sum_product = sum([dataset[user1][item] * dataset[user2][item] for item in both_rated])

    # Calculate the Pearson Correlation
    num = sum_product - (user1_total_rating*user2_total_rating/total_ratings)
    deno = sqrt((user1_squared_total - pow(user1_total_rating,2)/total_ratings) * (user2_squared_total -pow(user2_total_rating,2)/total_ratings))
    if deno == 0:
        return 0
    else:
        r = num/deno
        return r 
    
    
def predict_ratings(u1):

    
    totals = {}
    simSums = {}
   
    for u2 in dataset:
        # don't compare me to myself
        if u2 == u1:
            continue
        
        both_rated = {}
        for item in dataset[u1]:
            if item in dataset[u2]:
                both_rated[item] = 1

        total_ratings = len(both_rated)  
        user1_total_rating = sum([dataset[u1][item] for item in both_rated])
        user2_total_rating = sum([dataset[u2][item] for item in both_rated])
        
        user1_average_rating = round((user1_total_rating/total_ratings),2)
        user2_average_rating = round((user2_total_rating/total_ratings),2)
    
        sim = round(pearson_correlation(u1,u2),2)
        
        sim1 = abs(sim)
        print ("Correlation between",u1,u2,sim)

        for item in dataset[u2]:

            # only score movies i haven't seen yet
            if item not in dataset[u1] or dataset[u1][item] == 0:

            # CF Correlation score
                totals.setdefault(item,0)
                totals[item] = (totals[item] + (dataset[u2][item] - user2_average_rating) *sim)
                #print ("------>" ,totals[item])
                # sum of similarities
                simSums.setdefault(item,0)
                simSums[item]= (simSums[item] + sim1)
                #print("------>" ,simSums[item])
      
    rankings = [(round(((total/simSums[item]) + user1_average_rating),2),item) for item, total in totals.items()]
    
    return rankings

#Method to calculate Mean Absolute Error    
def mae(ratinglist): 
      
    list_size = len(ratinglist)
    item1 = ratinglist[0]
    ratingitem1 = concat(item1[1], item1[2])
    ratingitem1 = concat(ratingitem1, item1[3])
    ratingitem1 = concat(ratingitem1, item1[4])
    mprating_user1 = float(ratingitem1)
    
    item2 = ratinglist[1]
    ratingitem2 = concat(item2[1], item2[2])
    ratingitem2 = concat(ratingitem2, item2[3])
    ratingitem2 = concat(ratingitem2, item2[4])
    mprating_user2 = float(ratingitem2)
    
    item3 = ratinglist[2]
    ratingitem3 = concat(item3[1], item3[2])
    ratingitem3 = concat(ratingitem3, item3[3])
    ratingitem3 = concat(ratingitem3, item3[4])
    mprating_user3 = float(ratingitem3)
    
    item4 = ratinglist[3]
    ratingitem4 = concat(item4[1], item4[2])
    ratingitem4 = concat(ratingitem4, item4[3])
    ratingitem4 = concat(ratingitem4, item4[4])
    mprating_user4 = float(ratingitem4)
   
    mean_average_error = round(((abs(mprating_user1-4)+ abs(mprating_user2-3)+abs(mprating_user3-2)+abs(mprating_user4-5)) / list_size),2)
    
    return mean_average_error

#Method to calculate Root mean Square Error
def rmse(ratinglist): 
   
    list_size = len(ratinglist)
    item1 = ratinglist[0]
    ratingitem1 = concat(item1[1], item1[2])
    ratingitem1 = concat(ratingitem1, item1[3])
    ratingitem1 = concat(ratingitem1, item1[4])
    prating_user1 = float(ratingitem1)
    
    item2 = ratinglist[1]
    ratingitem2 = concat(item2[1], item2[2])
    ratingitem2 = concat(ratingitem2, item2[3])
    ratingitem2 = concat(ratingitem2, item2[4])
    prating_user2 = float(ratingitem2)
    
    item3 = ratinglist[2]
    ratingitem3 = concat(item3[1], item3[2])
    ratingitem3 = concat(ratingitem3, item3[3])
    ratingitem3 = concat(ratingitem3, item3[4])
    prating_user3 = float(ratingitem3)
    
    item4 = ratinglist[3]
    ratingitem4 = concat(item4[1], item4[2])
    ratingitem4 = concat(ratingitem4, item4[3])
    ratingitem4 = concat(ratingitem4, item4[4])
    prating_user4 = float(ratingitem4)
    
    rsmean_error = round(sqrt((pow((prating_user1-4),2)+pow((prating_user2-3),2)+pow((prating_user3-2),2) +pow((prating_user4-5),2)) / list_size),2)
    
    return rsmean_error
    
csvfile = "prediction.csv"
evalfile = "eval.csv"
ratings2 =[]


#Writing the prediction data to the prediction.csv file 
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    prating1 = 0
    for val in predict_ratings('Sammy'):
        writer.writerow(["Sammy"]+[val])  
        
with open(csvfile, "a") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in predict_ratings('Basil'):
        writer.writerow(["Basil"]+[val])    

                
with open(csvfile, "r") as pfile:
    readcsv = csv.reader(pfile)
    ratings2 = []
    for row in readcsv:
        user1 = row[1]
        ratings2.append(user1)
        
print ("MAE is: ", mae(ratings2))

print("RMSE is: ", rmse(ratings2))

pfile.close()

#Writing the evaluation data to the eval.csv file 
with open(evalfile, "w") as output2:
    writer = csv.writer(output2, lineterminator='\n')
    prating1 = 0
    val1 = mae(ratings2)
    writer.writerow(["MAE"]+[val1])
        
with open(evalfile, "a") as output2:
    writer = csv.writer(output2, lineterminator='\n')
    prating1 = 0
    val2 = rmse(ratings2)
    writer.writerow(["RMSE"]+[val2])
      

    


