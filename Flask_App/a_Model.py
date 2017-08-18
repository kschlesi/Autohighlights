from Flask_App import NLP
import pandas as pd

def apply_model(Xtrain = 'default', model= 'rfm', thresh = None, ntop=None):
    '''Applies model to training data from db'''

    # make predictions
    try:
        pred = model.predict_proba(Xtrain[Xtrain.columns[1:]])[:,1]
    except ValueError:
        # do a thing ... if no Xtrain
        print('no Xtrain...')
        raise
    Xtrain['pred'] = pred

    # grab highlights above threshold
    if ntop is not None:
        Xpred = Xtrain.sort_values('pred',ascending=False)
        Xorder = Xpred.iloc[0:ntop].sort_values('sposition')
    elif thresh is not None:
        Xorder = Xtrain[Xtrain.pred>thresh].sort_values('sposition')
    
    # if Xtop.empty()
    print(Xorder)
    h_index = list(Xorder[(Xorder.sposition.diff()==1)].index)
    h_index = list(set(h_index + [ix-1 for ix in h_index]))

    # get top 3 highest scored indices, OR top 2 and top group if any groups
    tops = Xorder.sort_values('pred',ascending=False).index
    recs = []
    grp_exists = False
    if len(h_index)==0:
        grp_exists = True
    for t in tops:  # go thru top indices in order
        if len(recs)<3:    
            if t in h_index: # add connected subset if in a group
                tlist = find_connected_subset(h_index,t)
                if tlist not in recs:
                    recs.append(tlist)
                grp_exists = True
            elif t not in h_index: # add it by self if not in group
                if len(recs)<2 or grp_exists:
                    recs.append([t])


    # grab top three highlights.
    try:
        hilites = [Xorder.loc[r] for r in recs]
    except KeyError:
        hilites = [Xorder.iloc[i] for i in range(3)]

    return [h[['apid','sposition']] for h in hilites]

def get_htext(recdflist=[],art_info=[]):
    '''taking highlightrecs and article info, returns htext dictionary of original sentences'''
    '''art_info is a df with three cols: ['postid', 'rawtext', 'origdb'] and only one row'''

    # gets unprocessed sentences for display
    sents = text_sentences(list(art_info.rawtext), origdb=3, keep_raw=True, to_stem=False)

    # grab position
    # recdflist is a list of three dataframes, one per highlight
    # htext takes the raw sentences corresponding to the list of recommended positions,
    # and joins them into a single string, for each of the three recommendation dataframes
    htext = ['. '.join([sents[0][i] for i in df.sposition]) for df in recdflist]
    #htext = [sents[0][spos] for spos in recdflist.sposition]
    htext_dict = dict(enumerate(htext))
    return htext_dict

def text_sentences(rawtext, origdb=3, keep_raw=True, to_stem=False):
    '''takes raw text and uses NLProcessor to break into sentences.
    can keep sentences raw for display or process and (optionally) stem'''
    sText = NLP.NLProcessor(rawtext)
    sText.process_text(break_on='.',init_split_on='database',
                       origdb=origdb,keep_raw=keep_raw,to_stem=to_stem)
    sents = sText.get_text()

    return sents

def find_connected_subset(inlist,start_value):
    ix = inlist.index(start_value)
    outlist = []
    outlist.append(start_value)
    while ix<len(inlist)-1 and inlist[ix+1]-inlist[ix]==1:
        ix = ix+1
        outlist.append(inlist[ix])
    ix = inlist.index(start_value)
    while ix>0 and inlist[ix]-inlist[ix-1]==1:
        ix = ix-1
        outlist.append(inlist[ix])
    outlist.sort()
    return outlist

