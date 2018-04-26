#!/usr/bin/env python3

from flask import Flask, flash, redirect, url_for, render_template, request

from flask_bootstrap import Bootstrap

from model import determine_phrase_or_word
# import model

app =Flask(__name__)
Bootstrap(app)


app.secret_key = 'hi secret key'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='GET':
        # flash('Please input your search:')
        timeframe_choice=['week', 'year', 'all', 'day', 'hour', 'month']
        sort_choice=['relevance', 'hot', 'top', 'new']
        return render_template('home.html', timeframe_choice=timeframe_choice, sort_choice=sort_choice)


    else:
        user_keywordphrase=request.form['keyword_or_phrase']
        user_subreddit=request.form['subreddit_choice']
        user_timeframe=request.form['timeframe_choice']
        user_sort=request.form['sort_choice']
        user_synonyms=request.form.get('include_synonyms')

        timeframe_choice=[ 'week', 'year', 'all', 'day', 'hour', 'month']
        sort_choice=['relevance', 'hot', 'top', 'new']

        if request.form.get('include_synonyms'):
            orig_links, reddit_links, list_ofsuggs= determine_phrase_or_word(user_keywordphrase, user_subreddit, user_timeframe, user_sort, strictness=False)
        else:
            orig_links, reddit_links, list_ofsuggs= determine_phrase_or_word(user_keywordphrase, user_subreddit, user_timeframe, user_sort, strictness=True)

        titleone="Reddit's Original Results"
        titletwo="Search n Rec Results"
        titlethree="Recommended Words Based on Sense2Vec:"
        # message2=" Just testing message2"
        iconl="icon-like"
        iconz="service-icon rounded-circle mx-auto mb-3"
        return render_template('home.html', timeframe_choice=timeframe_choice, sort_choice=sort_choice,
                               redditorig=orig_links, ourlist=reddit_links, wordrecs=list_ofsuggs,
                               titleone=titleone,
                               titletwo=titletwo, titlethree=titlethree,
                               iconl=iconl, iconz=iconz)
            # return (redirect(url_for('results')))




@app.route('/results', methods=['GET'])
def results():
    message2=" message 2 results page"
    #TODO display search results and recommendations
    return render_template('results.html', message2=message2)







if __name__=='__main__':
	# app.run(host='127.0.0.1', port=4000, debug=True)
	app.run(debug=True)
