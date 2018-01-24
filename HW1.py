import math

# Pads each sentence in the training and test corpora with start
# and end symbols (you can use <s> and </s>, respectively).
#
# Also lowercases all words in the training and test corpora.
#
def Padding(file):
    inFile = open(file, "r")
    in_text = inFile.read()
    inFile.close()
    outFile = open(file, "w")
    for line in in_text.split('\n'):
        sentence = "{0}" + line.lower().strip() + "{1}"
        outFile.write(sentence.format("<s> ", " </s>")+'\n')
    outFile.close()


# Counts the number of occurrences of a token in a text file
def count_words(word, filepath):
    data_in = open(filepath).read().split()
    count = data_in.count(word)
    return count


# Replace all words occurring in the training data once with the token <unk>. Every word
# in the test data not seen in training should be treated as <unk>.
def replace_tokens(filepath_in, filepath_out):
    inFile = open(filepath_in, "r").read().splitlines()
    outFile = open(filepath_out, "w")
    for word in inFile:
        if (count_words(word, filepath_in) == 1):
            word.replace(word, "<unk> ")
        else:
            word.replace(word, word + " ")
        outFile.write(word)
    inFile.close()
    outFile.close()

#Counts the total number of words in the corpus
def total_count(file):
    total = 0;
    readin = open(file, "r")
    in_text = readin.read()
    for line in in_text.split('\n'):
        for word in line.split():
            total += 1
    readin.close()
    return total


#Calculates the MLE of Unigram model
def Unigram(train,test):
    probability = 0;
    total_probability = 1;
    inFile1 = open(train, "r")
    total_words = total_count(train)
    in_text1 = inFile1.read().split()
    vocabulary1 = set(in_text1)
    vocab_list1 = list(vocabulary1)
    inFile2 = open(test, "r")
    in_text2 = inFile2.read().split()
    vocabulary2 = set(in_text2)
    vocab_list2 = list(vocabulary2)
    sentence = "Unigram: "
    parameters = "Unigram Parameters: "
    for word in vocabulary2:
        word_count = count_words(word, train)
        probability = word_count/ float(total_words)
        total_probability *= probability
        if word == vocab_list2[len(vocab_list2)-1]:
            sentence += str(probability) + " = "
            parameters += "P("+word+")"
        else:
            sentence += str(probability) + " * "
            parameters += "P("+word+")" + " * "
    print parameters
    print sentence + format(total_probability, '.50f')
    inFile1.close()
    inFile2.close()
    return total_probability


#Calculates the MLE of Bigram model
def Bigram(train,test):
    probability = 0;
    total_probability = 1;
    inFile1 = open(train, "r")
    in_text1 = inFile1.read()
    inFile2 = open(test, "r")
    in_text2 = inFile2.read()
    vocabulary_words1 = list(in_text1.split())
    vocabulary_words2 = list(in_text2.split())
    sentence = "Bigram: "
    parameters = "Bigram Parameters: "
    for index in range(len(in_text2.split())):
        if index == 0:
            word_count = count_words(vocabulary_words1[index], file)
            probability = word_count / float(total_count(file))
            total_probability *= probability
            sentence += str(probability) + " * "
            parameters += vocabulary_words2[index] + " * "
        else:
            if vocabulary_words2[index] == vocabulary_words2[len(vocabulary_words2)-1]:
                sentence += str(probability) + " = "
                parameters += vocabulary_words1[index-1] + " "+ vocabulary_words1[index] + " = "
            else:
                bigram_words = vocabulary_words1[index-1] + " "+ vocabulary_words1[index]
                bigram_count = bigram_check(bigram_words, file)
                if bigram_words <> "</s> <s>":
                    probability = bigram_count / float (count_words(vocabulary_words1[index-1],file))
                    total_probability *= probability
                    sentence += str(probability) + " * "
                    parameters += bigram_words + " * "
    print parameters
    print sentence + format(total_probability, '.50f')
    print '\n'
    inFile1.close()
    inFile2.close()
    return total_probability

#Calculates the MLE of Bigram Add_One_Smoothing model
def Add_One_Smoothing(train,test):
    probability = 0;
    total_probability = 1;
    inFile = open(file, "r")
    in_text = inFile.read()
    vocabulary_words = list(in_text.split())
    for index in range(len(in_text.split())):
        if index == 0:
            word_count = count_words(vocabulary_words[index], file) + 1
            probability = word_count / float(total_count(file) + len(vocabulary_words))
            total_probability *= probability
        else:
            bigram_words = vocabulary_words[index-1] + " "+ vocabulary_words[index]
            bigram_count = bigram_check(bigram_words, file) + 1
            if bigram_words <> "</s> <s>":
                probability = bigram_count / float (count_words(vocabulary_words[index-1],file) + len(vocabulary_words))
                total_probability *= probability
    print format(total_probability, '.50f')
    print '\n'
    inFile.close()


#Counts the number of occurrences of the bigram string in a text file
def bigram_check(words, file):
    data_in = open(file).read()
    count = 0;
    for line in data_in.split():
        if words in data_in:
            count += 1
    return count


#returns all the bigram tokens in a text file
def bigram_tokens(file):
    inFile = open(file, "r")
    in_text = inFile.read()
    vocabulary_words = list(in_text.split())
    new_list = []
    for index in range(len(in_text.split())):
        if index == 0:
            new_list.append(vocabulary_words[index])
        else:
            bigram_words = vocabulary_words[index-1] + " " + vocabulary_words[index]
            if bigram_words <> "</s> <s>":
                new_list.append(bigram_words)
    inFile.close()
    return new_list


#returns all bigram types in a text file
def bigram_types(file):
    new_list = list(bigram_tokens(file))
    return new_list

for word in open("brown-train.txt").read().split():
    print count_words(word, "brown-train.txt")

