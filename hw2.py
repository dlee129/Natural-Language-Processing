trained_unique_class = {}
trained_total_class = 0
trained_count_class = {}
unique_tokens = []
non_unique_tokens = []
trained_num_of_unique_tokens = 0
trained_total_tokens = {}
trained_vocabulary_prob_bag = {}
trained_vocabulary_prob_smoothing = {}


#NB classifier for Question1.1
def NBClassifier():
    pos_class = 0.4
    neg_class = 0.6
    pos_list = {}
    pos_list["I"] = 0.09
    pos_list["always"] = 0.07
    pos_list["like"] = 0.29
    pos_list["foreign"] = 0.04
    pos_list["films"] = 0.08
    neg_list = {}
    neg_list["I"] = 0.16
    neg_list["always"] = 0.06
    neg_list["like"] = 0.06
    neg_list["foreign"] = 0.15
    neg_list["films"] = 0.11
    pos_class_prob = pos_list["I"] * pos_list["always"] * pos_list["like"] * pos_list["foreign"] * pos_list["films"]
    print "P(pos) * P(S|pos) = P(I|pos) * P(always|pos) * P(like|pos) * P(foreign|pos) * P(films|pos)"
    print "= " + str(pos_list["I"]) + " * " + str(pos_list["always"]) + " * " + str(pos_list["like"]) + " * " + str(pos_list["foreign"]) + " * " + str(pos_list["films"])
    print "= " + str(pos_class_prob)+'\n'

    neg_class_prob = neg_list["I"] * neg_list["always"] * neg_list["like"] * neg_list["foreign"] * neg_list["films"]
    print "P(neg) * P(S|neg) = P(I|neg) * P(always|neg) * P(like|neg) * P(foreign|neg) * P(films|neg)"
    print "= " + str(neg_list["I"]) + " * " + str(neg_list["always"]) + " * " + str(neg_list["like"]) + " * " + str(neg_list["foreign"]) + " * " + str(neg_list["films"])
    print "= " + str(neg_class_prob)+'\n'
    if neg_class_prob > pos_class_prob:
        print "Naive Bayes Classifier: Negative Class"
    else:
        print "Naive Bayes Classifier: Positive Class"
    print '\n'


def train(file):
    inFile = open(file, "r")
    in_text = inFile.read()
    inFile.close()
    lines = in_text.splitlines()
    classes = [line.split()[-1] for line in lines]
    global trained_total_class
    trained_total_class = len(classes)

    for word in classes:
        if word not in trained_unique_class:
            trained_unique_class[word] = 1
            trained_count_class[word] = 1
        else:
            trained_unique_class[word] += 1
            trained_count_class[word] += 1

    #nested dictionaries for class types
    for class_dict in trained_unique_class:
        trained_unique_class[class_dict] = {}
        for line in lines:
            for word in line.split():
                if word not in trained_unique_class[class_dict]:
                    if word not in trained_unique_class:
                        if class_dict == line.split()[-1]:
                            trained_unique_class[class_dict][word] = 1
                else:
                    if word not in trained_unique_class:
                        if class_dict == line.split()[-1]:
                            trained_unique_class[class_dict][word] += 1


    #counts total number of tokens in unique classes
    for class_dict in trained_unique_class:
        tokens = 0
        for line in lines:
            for word in line.split():
                if word not in trained_unique_class:
                    if class_dict == line.split()[-1]:
                        tokens +=1
                trained_total_tokens[class_dict] = tokens

    #number of unique tokens in the corpus
    for word in in_text.split():
        if word not in trained_unique_class:
            non_unique_tokens.append(word)
    unique_tokens = set(non_unique_tokens)
    global trained_num_of_unique_tokens
    trained_num_of_unique_tokens = len(unique_tokens)

    #dictionary to hold probs of the bag of words
    for class_dict in trained_unique_class:
        trained_vocabulary_prob_bag[class_dict] = {}
        for word in trained_unique_class[class_dict]:
            trained_vocabulary_prob_bag[class_dict][word] = float(trained_unique_class[class_dict][word])/trained_total_tokens[class_dict]

    # dictionary to hold probs of the add one smoothing
    for class_dict in trained_unique_class:
        trained_vocabulary_prob_smoothing[class_dict] = {}
        for word in trained_unique_class[class_dict]:
            trained_vocabulary_prob_smoothing[class_dict][word] = (float(trained_unique_class[class_dict][word])+1) / (trained_total_tokens[class_dict] + trained_num_of_unique_tokens)




def test(file):
    inFile = open(file, "r")
    in_text = inFile.read()
    inFile.close()


    test_prob_bag = {}
    for word in in_text.split():
        for class_dict in trained_count_class:
            prob = float(trained_count_class[class_dict])/trained_total_class
            if word in trained_unique_class[class_dict]:
                prob = prob * trained_vocabulary_prob_bag[class_dict][word]
        test_prob_bag[class_dict] = prob
    print test_prob_bag

    test_prob_smoothing = {}
    for class_dict in trained_count_class:
        prob = float(trained_count_class[class_dict])/trained_total_class
        for word in trained_unique_class[class_dict]:
            prob = prob * trained_vocabulary_prob_smoothing[class_dict][word]
        test_prob_smoothing[class_dict] = prob
    print test_prob_smoothing



# Notes for hw
#     Small training corpus which is the five lines A to E
#     Last word is the class for each line
#     Implement bag of words = check for every word in vocabulary that occurred
#     P(comedy) = 2/5 * P of each feature P(word | comedy)
#     P(action) = 3/5 * P of each feature P(word | action)
#     V = {fun, couple, love, fast, furious, shoot, fly}
#     p(a|b) = c(b,a)/c(b)

NBClassifier()
train("movie-review.NB")
test("document.NB")