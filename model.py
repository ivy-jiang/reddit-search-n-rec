#!/usr/bin/env python3
from collections import defaultdict, Counter
import string
# import en_core_web_md
import spacy

# from spacy import vocab, is_lower, prob, similarity
# nlp = en_core_web_md.load()
nlp = spacy.load('en')
# nlp= spacy.load('en_core_web_md')

from sense2vec import Sense2VecComponent
s2v = Sense2VecComponent('reddit_vectors-1.1.0')

# s2v = Sense2VecComponent('/mnt/c/Users/ivy1g/Documents/proj/weventy/reddit_vectors-1.1.0')
nlp.add_pipe(s2v)

import praw
####TODO TODO TODO ##INSERT praw.REDDIT CLIENT ID< SECRET< USER_AGENT

## http://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html

def get_related(word):
  filtered_words = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
  similarity = sorted(filtered_words, key=lambda w: word.similarity(w), reverse=True)
  return similarity[:2]

def create_syns(searchterm, yesassert=False):
    searchtermz=str(searchterm)
    list_lexemeobj=get_related(nlp.vocab[u'{}'.format(searchtermz)])
    if yesassert != False:
        tokenlist=[]
        pos_tags=['{}'.format(yesassert)]
        for w in list_lexemeobj:
            myword=w.lower_
            doc= nlp(u'{}'.format(myword))
            for token in doc:
                tokenlist.append(token)
        print (tokenlist)
        for i in tokenlist:
            print(i.pos_)
        vocab = filter(lambda x: x.pos_ in pos_tags, tokenlist)
    list_ofwords_dup=[w.lower_ for w in list_lexemeobj]
    seen = set()
    list_ofwords = []
    for item in list_ofwords_dup:
        if item not in seen:
            seen.add(item)
            list_ofwords.append(item)
    return list_ofwords[:2]

def maker_clean(meword):
    aggregatelist=[]
    mewordl=list(meword)
    mewordnew=meword
    mewcp=meword
    for c in mewordl:
        if c.isupper():
            mewordnew=mewcp.casefold()
            print("new meword", mewordnew)
            break
    if mewordnew == meword:
        mewordnew=meword.title()
        print("new meword", mewordnew)

    docit = nlp(u"{}".format(mewordnew))
    for tokit in docit:
        if tokit.ent_type_:
            for entit in docit.ents:
                try:
                    assert entit._.in_s2v
                    most_similarit = entit._.s2v_most_similar(5)
                    aggregatelist.append(most_similarit)
                except:
                    print("really fails")
        else:
            try:
                assert tokit._.in_s2v
                most_similarit = tokit._.s2v_most_similar(5)
                aggregatelist.append(most_similarit)
            except:
                print("really fails")
    print("this is it", aggregatelist)
    return aggregatelist

def maker_sense2vec(meword):

    aggregatelist=[]
    doc = nlp(u"{}".format(meword))
    for token in doc:
        # print("what token is ", token.dep_)
        # print("tag:",token.tag_,"pos:", token.pos_, "enttype:", token.ent_type_, "lemma:", token.lemma_, )
        # tag = token.ent_type_ or token.pos_
        if token.ent_type_:
            print(token.text , "is entity", token.ent_type_)
            for ent in doc.ents:
                # print(ent.text, ent.start_char, ent.end_char, ent.label_)
                try:
                    assert ent._.in_s2v
                    most_similar = ent._.s2v_most_similar(12)
                    aggregatelist.append(most_similar)
                except:
                    print('error in ents.....')
                    texttodeal=token.text
                    deallist=texttodeal.split()
                    for i in deallist:
                        doci = nlp(u"{}".format(i))
                        for tokeni in doci:
                            if tokeni.ent_type_:
                                for enti in doci.ents:
                                    try:
                                        assert enti._.in_s2v
                                        most_similari = enti._.s2v_most_similar(5)
                                        aggregatelist.append(most_similari)
                                    except:
                                        #TODO
                                        mewor=tokeni.text
                                        listtoadd= maker_clean(mewor)
                                        if listtoadd != []:
                                            print("ok added something.")
                                            aggregatelist+=listtoadd
                            else:
                                try:
                                    assert tokeni._.in_s2v
                                    most_similari = tokeni._.s2v_most_similar(5)
                                    aggregatelist.append(most_similari)
                                except:
                                    #TODO
                                    mewor=tokeni.text
                                    listtoadd= maker_clean(mewor)
                                    if listtoadd != []:
                                        print("ok added something.")
                                        aggregatelist+=listtoadd

        else:
            print(token.text , "is pos normal", token.pos_)
            try:
                assert token._.in_s2v
                most_similar = token._.s2v_most_similar(12)
                aggregatelist.append(most_similar)
            except:
                print('error in pos')
                texttodeal=token.text
                deallist=texttodeal.split()
                for i in deallist:
                    doci = nlp(u"{}".format(i))
                    for tokeni in doci:
                        if tokeni.ent_type_:
                            for enti in doci.ents:
                                try:
                                    assert enti._.in_s2v
                                    most_similari = enti._.s2v_most_similar(5)
                                    aggregatelist.append(most_similari)
                                except:
                                    #TODO
                                    mewor=tokeni.text
                                    listtoadd= maker_clean(mewor)
                                    if listtoadd != []:
                                        print("ok added something.")
                                        aggregatelist+=listtoadd
                        else:
                            try:
                                assert tokeni._.in_s2v
                                most_similari = tokeni._.s2v_most_similar(5)
                                aggregatelist.append(most_similari)
                            except:
                                #TODO
                                mewor=tokeni.text
                                listtoadd= maker_clean(mewor)
                                if listtoadd != []:
                                    print("ok added something.")
                                    aggregatelist+=listtoadd
    synonymlist=[]
    for eachlist in aggregatelist:
        for eachtuple in eachlist:
            synonymlist.append(eachtuple[0][0])
    seen = set()
    list_ofwords = []
    for item in synonymlist:
        if item not in seen:
            seen.add(item)
            list_ofwords.append(item)
        else:
            Z="REMOVED DUPLICATE"
    return list_ofwords



# Most basic existing search
def searchterm_in_subreddit(searchterm, list_ofwords, mysubreddit, timef, sortc):
    searchtermz=str(searchterm)
    # list_lexemeobj=get_related(nlp.vocab[u'{}'.format(searchtermz)])
    # list_ofwords=[w.lower_ for w in list_lexemeobj]
    all_listing_threads=[]
    #TODO change limit to 100 but now just 2
    for i in range (len(list_ofwords)):
        if list_ofwords[i] == searchtermz:
            # for submission in reddit.subreddit('{}'.format(mysubreddit)).search('{}'.format(list_ofwords[i]), time_filter="month", limit=5, sort='top'):
            for submission in reddit.subreddit('{}'.format(mysubreddit)).search('{}'.format(list_ofwords[i]), time_filter="{}".format(timef), limit=5, sort='{}'.format(sortc)):

                all_listing_threads.append(submission)
                # print (submission.title, submission.score, submission.upvote_ratio, submission.num_comments)

        else:
            for submission in reddit.subreddit('{}'.format(mysubreddit)).search('{}'.format(list_ofwords[i]), time_filter="{}".format(timef), limit=1, sort='{}'.format(sortc)):
                if submission not in all_listing_threads:
                    all_listing_threads.append(submission)

                # print (submission.title, submission.score, submission.upvote_ratio, submission.num_comments)
            # print (submission.score, submission.ups, submission.num_comments)
    return all_listing_threads
    # print (all_listing_threads, len(all_listing_threads))

def get_allcomments(all_listing_threads):
    listofwordsdict=[]
    for submission in all_listing_threads:
        each_thread_dict = {}
        submission.comments.replace_more(limit=2)
        for comment in submission.comments.list():
            # print(comment.body)
            if comment.id not in each_thread_dict:
                each_thread_dict[comment.id] = [comment.body,{}]
                if comment.parent() != submission.id:
                    parent = str(comment.parent())
                    each_thread_dict[parent][1][comment.id] = [comment.body]

        listofwordsdict.append(each_thread_dict)
    print ([len(dict) for dict in listofwordsdict])
    return (listofwordsdict)
    # print(len(conversedict))
    # print(list(conversedict.items())[11])
    # print(reddit.comment(id='dwwusag').body, reddit.comment(id='dwwusag').ups)



# def pick_submission_comments_upvotes(listing_from_search, n_times):
def pick_submission_comments_upvotes(all_listing_threads):
    listoftuplesvotes=[]
    for potential_submission in all_listing_threads:
    #    stitle, sauthor, slink = (potential_submission.title, potential_submission.author, potential_submission.url)
        slink=potential_submission.url
        svote= potential_submission.upvote_ratio
        sscore=potential_submission.score
        snumcom=potential_submission.num_comments
        listoftuplesvotes.append((slink, svote, sscore, snumcom))
        numcomments= potential_submission.num_comments
    sortedbyups= sorted(listoftuplesvotes, key=lambda x:x[1], reverse=True)
    list_subs_upvotes=sortedbyups[:3]
    sortedbyscore= sorted(listoftuplesvotes, key=lambda x:x[2], reverse=True)
    list_subs_score=sortedbyscore[:3]
    sortedbynumcom= sorted(listoftuplesvotes, key=lambda x:x[3], reverse=True)
    list_subs_numcom=sortedbynumcom[:3]
    return list_subs_upvotes, list_subs_score, list_subs_numcom

def countphraseocc(listofwordz, listofwordsdict, all_listing_threads):
    submissionids=[submission.id for submission in all_listing_threads]
    # EACH THREAD
    pos_counts = {}
    for each_thread_dict in listofwordsdict:
        for keyid,value in each_thread_dict.items():
            commentkey = reddit.comment(id=keyid)
            if commentkey.parent() in submissionids:
                ## Original comment <<STRING>>
                originalcomment= value[0]
                replies_tooriginal=value[1]
                for wordtofind in listofwordz:
                    # print("wordtofind????", wordtofind)
                    origclean=originalcomment.casefold()
                    origclean=origclean.translate(str.maketrans('','',string.punctuation))
                    if wordtofind in origclean:
                        if str(commentkey.parent()) in pos_counts:
                            if keyid in pos_counts[str(commentkey.parent())]:
                                pos_counts[str(commentkey.parent())][keyid].append(keyid)
                            else:
                                pos_counts[str(commentkey.parent())][keyid]=[keyid,]
                        else:
                            pos_counts[str(commentkey.parent())]={}
                            pos_counts[str(commentkey.parent())][keyid]=[keyid,]

                for replyzid,votes_body in replies_tooriginal.items():
                    ## Original comment RRRRREPLIES <<STRING>>
                    replybody=votes_body[0]
                    for wordtofind in listofwordz:
                        origclean=replybody.casefold()
                        origclean=origclean.translate(str.maketrans('','',string.punctuation))
                        if wordtofind in origclean:
                            if str(commentkey.parent()) in pos_counts:
                                if keyid in pos_counts[str(commentkey.parent())]:
                                    pos_counts[str(commentkey.parent())][keyid].append(replyzid)
                                else:
                                    pos_counts[str(commentkey.parent())][keyid]=[replyzid,]
                            else:
                                pos_counts[str(commentkey.parent())]={}
                                pos_counts[str(commentkey.parent())][keyid]=[replyzid,]
    # print(pos_counts, "postcounts????????????")
    # for keysub, valz in pos_counts.items():
    for submission in submissionids:
        submissionitself = reddit.submission(id="{}".format(submission))
        subtextitself=submissionitself.selftext
        subtitle=submissionitself.title
        subtextclean=subtextitself.casefold()
        subtextclean=subtextclean.translate(str.maketrans('','',string.punctuation))
        subtitleclean=subtitle.casefold()
        subtitleclean=subtitleclean.translate(str.maketrans('','',string.punctuation))
        # print ("SUBTEXXXT ITSELF", subtextclean)
        for wordtofind in listofwordz:
            if wordtofind in subtextclean or wordtofind in subtitleclean:
                if submission in pos_counts:
                    if submission in pos_counts[submission]:
                        pos_counts[submission][submission].append("OP post")
                    else:
                        pos_counts[submission][submission]=["OP post",]
                else:
                    pos_counts[submission]={}
                    pos_counts[submission][submission]=["OP post",]
    return pos_counts

def comment_countwordocc(list_ofwords, listofwordsdict, all_listing_threads):
    submissionids=[submission.id for submission in all_listing_threads]
    # EACH THREAD
    pos_counts = {}
    for each_thread_dict in listofwordsdict:
        # EACH THREAD's ALL COMMENTS
        for keyid,value in each_thread_dict.items():
            commentkey = reddit.comment(id=keyid)
            if commentkey.parent() in submissionids:
                ## Original comment <<STRING>>
                originalcomment= value[0]
                texttosearch = nlp(u'{}'.format(originalcomment))
                for wordtofind in list_ofwords:
                    wordnlp=nlp(u'{}'.format(wordtofind))
                    for token in wordnlp:
                        if token.text in [tok.text for tok in texttosearch]:
                            if str(commentkey.parent()) in pos_counts:
                                if keyid in pos_counts[str(commentkey.parent())]:
                                    pos_counts[str(commentkey.parent())][keyid].append(keyid)
                                else:
                                    pos_counts[str(commentkey.parent())][keyid]=[keyid,]
                            else:
                                pos_counts[str(commentkey.parent())]={}
                                pos_counts[str(commentkey.parent())][keyid]=[keyid,]

                replies_tooriginal=value[1]
                for replyzid,votes_body in replies_tooriginal.items():
                    ## Original comment RRRRREPLIES <<STRING>>
                    replybody=votes_body[0]
                    twotexttosearch = nlp(u'{}'.format(replybody))
                    for wordtofind in list_ofwords:
                        wordnlp=nlp(u'{}'.format(wordtofind))
                        for token in wordnlp:
                            if token.text in [tok.text for tok in twotexttosearch]:
                                if str(commentkey.parent()) in pos_counts:
                                    if keyid in pos_counts[str(commentkey.parent())]:
                                        pos_counts[str(commentkey.parent())][keyid].append(replyzid)
                                    else:
                                        pos_counts[str(commentkey.parent())][keyid]=[replyzid,]
                                else:
                                    pos_counts[str(commentkey.parent())]={}
                                    pos_counts[str(commentkey.parent())][keyid]=[replyzid,]
            else:
                pass
    # for keysub, valz in pos_counts.items():
    for submission in submissionids:
        submissionitself = reddit.submission(id="{}".format(submission))
        subtextitself=submissionitself.selftext
        subtitle=submissionitself.title
        itselftosearch = nlp(u'{}'.format(subtextitself))
        titletosearch = nlp(u'{}'.format(subtitle))
        for wordtofind in list_ofwords:
            wordnlp=nlp(u'{}'.format(wordtofind))
            for token in wordnlp:
                if token.text in [tok.text for tok in itselftosearch] or token.text in [tok.text for tok in titletosearch]:
                #     pos_counts[keysub][keysub]=["OP post",]
                # if token.text in [tok.text for tok in titletosearch]:
                    if submission in pos_counts:
                        if submission in pos_counts[submission]:
                            pos_counts[submission][submission].append("OP post")
                        else:
                            pos_counts[submission][submission]=["OP post",]
                    else:
                        pos_counts[submission]={}
                        pos_counts[submission][submission]=["OP post",]

    return pos_counts


def comment_upvotescore(dict_countword):
    subs_counter=defaultdict(list)
    for keyie, valuesie in dict_countword.items():
        for tierone_id, list_ids in valuesie.items():
            own_tier=[]
            upvotetotal_tier=0
            for itemid in list_ids:
                if itemid == 'OP post':
                    # reddit_include= reddit.submission(id="{}".format(tierone_id))
                    # n_upvote=reddit_include.score
                    combo=tierone_id, "OP includes"
                    own_tier.append(combo)
                else:
                    reddit_include= reddit.comment(id="{}".format(itemid))
                    n_upvote=reddit_include.score
                    combo=itemid, n_upvote
                    own_tier.append(combo)
                    upvotetotal_tier+=n_upvote
            subs_counter[tierone_id].append(upvotetotal_tier)
            subs_counter[tierone_id].append(own_tier)
                #basically each tier one reps COMMENT tree
    return subs_counter


def topcomm_wordincl_votes(dict_upvote, topn=10):
    our_dict=dict(dict_upvote)
    listdict=list(our_dict.items())
    sortlist_upvotes= sorted(our_dict, key= lambda x: (our_dict[x][0]), reverse=True)
    masterlist=[]
    if len(sortlist_upvotes)<topn:
        my_n=len(sortlist_upvotes)
    else:
        my_n=topn
    print("TOP n posts: ", my_n)
    for i in range(my_n):
        medict={}
        origcomid= sortlist_upvotes[i]
        medict[origcomid]=[]
        numchild=len(our_dict[origcomid][1])
        for z in range(numchild):
            actualcomid=our_dict[origcomid][1][z][0]
            medict[origcomid].append(actualcomid)
        masterlist.append(medict)
    return masterlist


def construct_reddit_links(masterlist_ofids, all_listing_threads):
    submissionids=[submission.id for submission in all_listing_threads]
    redditlinklist=[]

    for origdict in masterlist_ofids:
        for key,val in origdict.items():
            if key in submissionids:
                pass
                # subredz=str(key.subreddit)
                # permal=key.permalink
                # redditlink="https://www.reddit.com"+ permal
                # redditlink="https://www.reddit.com/r/{}/comments/".format(subredz)
                # newstr=redditlink+key
                # redditlinklist.append(redditlink)

            else: ######### RETURNS MOST AGGREGATE VOTED PARENT COMMENT ##########3
                commentkey = reddit.comment(id=key)
                permal=commentkey.permalink
                redditlink="https://www.reddit.com"+permal
                # subredz=str(commentkey.subreddit)
                # redditlink="https://www.reddit.com/r/{}/comments/".format(subredz)
                # subid= str(commentkey.parent())
                # newstring=redditlink+subid+'//'+key
                redditlinklist.append(redditlink)

                # redditlinklist.append(newstring)
                # for i in range (len(val)):
                #     newstr=redditlink+subid+'//'+val[i]
                #     redditlinklist.append(newstr)

    return redditlinklist

def orig_reddit_links(all_listing_threads):
    submissionids=[submission.id for submission in all_listing_threads]
    oredditlinklist=[]
    for submi in all_listing_threads:
        permal=submi.permalink
        redditlink="https://www.reddit.com"+permal
        # subredz=str(submi.subreddit)
        # submiid=str(submi.id)
        # redditlink="https://www.reddit.com/r/{subred}/comments/{subid}".format(subred=subredz, subid=submiid)
        oredditlinklist.append(redditlink)
    return oredditlinklist



def start_inputphrase(searchterm, subred, timef, sortc, strictness):
    # searchterm="running a marathon".casefold()
    searchterm=searchterm.casefold()
    # subred="nba"
    # timef="year"
    # sortc="relevance"
    list_ofsuggs= maker_sense2vec(searchterm)
    if len(list_ofsuggs)<1:
        searchtermtitle=searchterm.title()
        listcompare=maker_sense2vec(searchtermtitle)
        list_ofsuggs= listcompare


    if strictness == False:
        print("NOT STRICT... getting individual words from phrase")
        newsearchlist=[searchterm, ]
        wordnlp=nlp(u'{}'.format(searchterm))
        for token in wordnlp:
            if token.is_stop:
                pass
            elif token.text == searchterm:
                # print(token.text, searchterm, "should be the same so not double appending")
                melemma=token.lemma_
                # print("LEMMA:   ", melemma, "WHILE string text is,  ", token.text)
                if melemma:
                    if melemma != token.text and melemma not in newsearchlist:
                        # ("NOT EQUALS!!! so added to newsearchlist.... ")
                        newsearchlist.append(melemma)
            else:
                newsearchlist.append(token.text)
                melemma=token.lemma_
                # print("KEYWORDDD TERMMMM LEMMA:   ", melemma, "WHILE string text is,  ", token.text)
                if melemma:
                    if melemma != token.text and melemma not in newsearchlist:
                        # ("NOT EQUALS!!! so added to newsearchlist.... ")
                        newsearchlist.append(melemma)
        meslist=searchterm.split()
        # print("indiv splitup: ", meslist)
        for i in meslist:
            if i not in newsearchlist:
                newsearchlist.append(i)
    else:
        print("STRICT.. just the phrase")
        newsearchlist=[searchterm, ]

    print("list to be searched:   ", newsearchlist)
    all_listing_threads= searchterm_in_subreddit(searchterm, newsearchlist, subred, timef, sortc)
    print (all_listing_threads)
    listofwordsdict=get_allcomments(all_listing_threads)
    # print ("listofwordsdict    ", listofwordsdict)
    dict_countword= countphraseocc(newsearchlist, listofwordsdict, all_listing_threads)
    dict_upvote=comment_upvotescore(dict_countword)
    masterlist_ofids=topcomm_wordincl_votes(dict_upvote, topn=5)
    reddit_links= construct_reddit_links( masterlist_ofids, all_listing_threads)
    orig_links= orig_reddit_links(all_listing_threads)
    return orig_links, reddit_links, list_ofsuggs

def start_inputkeyword(searchterm, subred, timef, sortc, strictness):
    searchterm=searchterm.casefold()
    list_ofsuggs= maker_sense2vec(searchterm)
    if len(list_ofsuggs)<1:
        searchtermtitle=searchterm.title()
        listcompare=maker_sense2vec(searchtermtitle)
        list_ofsuggs= listcompare
    list_ofsuggs_two=list_ofsuggs[:3] #TODO
    if strictness == False:
        print("NOT STRICT.. getting syns FOR WORD")
        list_ofwords= list_ofsuggs_two
        wordnlp=nlp(u'{}'.format(searchterm))
        for token in wordnlp:
            melemma=token.lemma_
            # print("WORDDDD LEMMA:   ", melemma, "WHILE string text is,  ", token.text)
            if melemma:
                if melemma != token.text and melemma not in list_ofwords:
                    # ("NOT EQUALS!!! so added to listofwords.... ")
                    list_ofwords.append(melemma)
        if searchterm not in list_ofwords:
            list_ofwords.append(searchterm)
    else:
        print("STRICT no syns.. just literal WORD ")
        list_ofwords=[searchterm, ]
    # list_ofwords=create_syns(searchterm)

    print("listofwords: ", list_ofwords)
    all_listing_threads= searchterm_in_subreddit(searchterm, list_ofwords, subred, timef, sortc)
    print (all_listing_threads)
    listofwordsdict=get_allcomments(all_listing_threads)
    dict_countword=comment_countwordocc(list_ofwords, listofwordsdict, all_listing_threads)
    # print ("***********dictwordcount   ", dict_countword)
    dict_upvote=comment_upvotescore(dict_countword)
    masterlist_ofids=topcomm_wordincl_votes(dict_upvote, topn=5)
    reddit_links= construct_reddit_links( masterlist_ofids, all_listing_threads)
    orig_links= orig_reddit_links(all_listing_threads)

    return orig_links, reddit_links, list_ofsuggs

def determine_phrase_or_word(searchterm, subred, timef, sortc, strictness):
    user_input=str(searchterm)
    list_str=user_input.split()
    if len(list_str)> 1:
        #phrase
        print("PHRASE!")
        result = start_inputphrase(searchterm, subred, timef, sortc, strictness)
        return result
    else:
        #word
        print("WORD!")
        result= start_inputkeyword(searchterm, subred, timef, sortc, strictness)
        return result



if __name__ == "__main__":
    # user_keywordphrase="lebron james plays defense"
    # user_keywordphrase="plays"

    user_subreddit="nba"
    user_timeframe="day"
    user_sort="relevance"

    liss=maker_sense2vec("lebron")
    print (liss)

    # print("********************")
    # liss2=maker_sense2vec("Lebron")
    # print (liss2)
    # print ("Westbrook" == "Westbrook")

    # list_ofsuggs= maker_sense2vec(searchterm)
    # if len(list_ofsuggs)<1:
    #     searchtermtitle=searchterm.title()
    #     listcompare=maker_sense2vec(searchtermtitle)
    #     list_ofsuggs= listcompare
    # orig_links, reddit_links, list_ofsuggs= determine_phrase_or_word(user_keywordphrase, user_subreddit, user_timeframe, user_sort, strictness=False)
    # print("Results****************", orig_links, reddit_links, list_ofsuggs)


    # print (start_inputphrase(strictness=True))
    # print (start_inputphrase("shooting guard", "nba", "year", "relevance", strictness=False))

    # print (start_inputkeyword("eat", "xxfitness", "year", "relevance", strictness=False))

    # print(create_syns("duck"))
    # print(create_syns("running"))

    # dict_countword= countphraseocc(list_ofwords, searchterm, listofwordsdict, all_listing_threads)

    # list_subs_upvotes, list_subs_score, list_subs_numcom= pick_submission_comments_upvotes(cardio_all_listing_threads)

    # dict_upvote={'dvv5rlq': [1, [('dvv79ot', 1)]], 'dwgdcfz': [60, [('dwgdcfz', 60)]], 'dwh10q3': [3, [('dwh10q3', 3)]], 'dvv46sq': [20, [('dvv46sq', 20)]], 'dwgwqt7': [2, [('dwgwqt7', 2)]], 'dvv1zg5': [3, [('dvv6keb', 3)]], 'dvvgf7a': [9, [('dvvgf7a', 5), ('dvvh2yk', 4)]], 'dvw2ce9': [1, [('dvw2ce9', 1)]], 'dvuz7sm': [4, [('dvuz7sm', 4)]], '8561g1': [0, [('8561g1', 'OP includes')]], 'dwgz1my': [3, [('dwgzcrj', 3)]], '87wm7f': [0, [('87wm7f', 'OP includes'), ('87wm7f', 'OP includes')]], 'dwg9pao': [2, [('dwh3caz', 2)]]}
    # masterlist_ofids= topcomm_wordincl_votes(dict_upvote)

    #TODO TODO # TODO: if empty list after wordcount
    #
    # all_listing_threads= searchterm_in_subreddit("eat", ["eat", "food"], "xxfitness", "year", "relevance")
    # print (orig_reddit_links(all_listing_threads))

    # subred="nba"
    # timef="year"
    # sortc="relevance"
