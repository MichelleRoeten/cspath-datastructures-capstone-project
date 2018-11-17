from linkedlist import LinkedList


class Trie:

    def __init__(self, debug=False):
        self.head_node = TrieNode(None)
        self.debug = debug

    def get_head_node(self):
        return self.head_node

    def add_word(self, mixed_case_word):
        if mixed_case_word == None:
            word = None
        else:
            word = mixed_case_word.lower()  # Convert all letters to lower case before adding them to the trie.
        if self.debug == True:
            level = 0
            print('Adding \'{0}\'...'.format(word))
        current_node = self.get_head_node()
        letters_processed = 0
        word_letter_count = len(word)
        for letter in word:
            letters_processed += 1
            current_letter = current_node.get_letter()
            current_children = current_node.get_children()
            match_found = False
            for child in current_children:
                child_letter = child.get_letter()
                if child_letter == letter:
                    match_found = True
                    if letters_processed == word_letter_count:
                        if child.get_word() == None:
                            child.set_word(word)
                            if self.debug == True:
                                print('We just marked {0}, already in the Trie, as a completed word!'.format(word))
                        else:
                            if self.debug == True:
                                print('The word {0} is already in the Trie!'.format(word))
                    current_node = child
                    break
            if match_found == False:
                if self.debug == True:
                    level += 1
                    print('Adding {0} to level {1} under letter {2}.'.format(letter, str(level), current_letter))
                current_node = current_node.add_child(letter)
                if letters_processed == word_letter_count:  # We've come to the end of the word.
                    if current_node.get_word() == None:     # No word has been stored at this node yet.
                        current_node.set_word(word)
                        if self.debug == True:
                            print('We just completed adding the word \'{0}\'!'.format(word))
        return current_node

    def get_words(self, search_string):
        if search_string == None:
            prefix = None
        else:
            prefix = search_string.lower() # convert to lower case to ensure match
        matching_words = []
        match_found = False
        # First navigate to the node representing the completed prefix.
        current_node = self.get_head_node()
        letters_processed = 0
        prefix_letter_count = len(prefix)
        for letter in prefix:
            letters_processed += 1
            current_children = current_node.get_children()
            match_found = False
            for child in current_children:
                child_letter = child.get_letter()
                if child_letter == letter:
                    match_found = True
                    if letters_processed == prefix_letter_count:
                        if child.word_found():
                            matching_words.append(prefix)
                if match_found == True:
                    current_node = child
                    break               
        # Next, traverse all the children to get remaining matches.
        if match_found == True or prefix == '':
            matching_words = self.traverse_the_trie(current_node, matching_words)
        return(matching_words)

    def traverse_the_trie(self, node, words):
        current_children = node.get_children()
        for child in current_children:
            next_letter = child.get_letter()
            if child.word_found():
                words.append(child.word)
            result = self.traverse_the_trie(child, words)
        return words


class TrieNode:
    
    def __init__(self, letter):
        self.letter   = letter
        self.children = []
        self.word     = None  # contains a value when the letter stored in this node completes a word
                              #   if you traverse the tree from the top to here
        self.data     = None  # consists of a linked list containing data associated with the word if
                              #   there is one

    def get_letter(self):
        return self.letter

    def add_child(self, letter):
        child = TrieNode(letter)
        self.children.append(child)
        return child

    def get_children(self):
        return self.children

    def set_word(self, word):
        self.word = word

    def get_word(self):
        return self.word

    def word_found(self):
        return self.word is not None

    def add_data(self, data):
        if self.data == None:
            self.data = LinkedList(data)
        else:
            self.data.insert_beginning(data)

    def get_data(self):
        return self.data


class RestaurantSearchEngine(Trie):

    def add_type(self, restaurant_type):
        self.add_word(restaurant_type)

    def add_restaurant(self, restaurant_data):
        # restaurant_data is a list containing [type, name, price, rating, address]
        restaurant_type = restaurant_data[0].lower()
        restaurant_details = restaurant_data[1:]
        restaurant_list_node = self.add_word(restaurant_type)
        restaurant_list_node.add_data(restaurant_details)

    def display_restaurants(self, type):
        if type == None:
            restaurant_type = None
        else:
            restaurant_type = type.lower()
        current_node = self.head_node
        letter_string = ''
        match_found = False
        for letter in restaurant_type:
            children = current_node.get_children()
            match_found = False
            for child in children:
                if letter == child.get_letter():
                    letter_string += letter
                    current_node = child
                    match_found = True
                if match_found == True:
                    break
        if match_found == True:
            restaurant_list = current_node.get_data()
            if restaurant_list == None:
                print('\nIt looks like you may have made a typo.  Please start over.')
            else:
                print('\nThe {0} Restaurants in SoHo are:'.format(restaurant_type.capitalize()))
                formatted_list = ''
                current_node = restaurant_list.head_node
                while current_node:
                    formatted_list += '\n-----------------------------\n'
                    formatted_list += '\nName:    '
                    formatted_list += current_node.value[0]
                    formatted_list += '\nPrice:   '
                    formatted_list += current_node.value[1]
                    formatted_list += '\nRating:  '
                    formatted_list += current_node.value[2]
                    formatted_list += '\nAddress: '
                    formatted_list += current_node.value[3]
                    formatted_list += '\n'
                    current_node = current_node.get_next_node()
                print(formatted_list)
