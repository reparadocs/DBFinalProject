import math
import operator

def cosineSimilarity(ratings_table, users, movie1, movie2):
    numerator = 0.
    denom1 = 0.
    denom2 = 0.
    for u in users:
    	if (u, movie1) in ratings_table and (u, movie2) in ratings_table:
    		r1 = ratings_table[u, movie1]
    		r2 = ratings_table[u, movie2]
	        numerator += r1 * r2
	        denom1 += r1**2.0
	        denom2 += r2**2.0
	denom = math.sqrt(denom1 * denom2)
	if denom == 0:
		return 0.
    return numerator / denom

def itemPrediction(ratings_table, user_id, movie_id, users, movies):
    k = 0.
    s = 0.
    for m in movies:
        if m != movie_id:
        	cos_sim = cosineSimilarity(ratings_table, users, movie_id, m)
        	if (user_id, m) in ratings_table:
        		s += cos_sim * ratings_table[user_id, m]
        	else:
        		s += cos_sim
        		k += abs(cos_sim)
    if k == 0:
    	return 0.
    k = 1.0 / k
    return k * s

def recommendMovies(ratings_table, user_id, users, movies, N=4):
	i = 0
	predicts = {}
	recommended = []
	for m in movies:
		if i%10 == 0:
			prediction = itemPrediction(ratings_table, user_id, m, users, movies)
			predicts[m] = prediction
		i+=1
	sort = sorted(predicts.items(), key=operator.itemgetter(1), reverse=True)[:N]
	for s in sort:
		recommended.append(s[0])
	# print(recommended)
	return recommended



