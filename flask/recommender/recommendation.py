import json
import numpy as np
from lightfm.data import Dataset
from lightfm import LightFM
import scipy.sparse as sp

def lightfmReccomend(interact,postdetail):
    # print(interact)
    useridi = 1
    ppid = [] # all post ids
    iuid = [] # all user ids (same)
    related = [] # all post user releted (interaction > 1)
    tags = [] # all post tags
    inumber = []
    allinteractions = [] # all interactions
    nametags = ("Dogs","Cats","Fishes","Mammals","Insects","Reptiles","Birds","Amphibians",)
    etags = [] #all tags multi


    def convertPost(interact,postdetail):
        
        count = -1
        for post in postdetail:
            # print(post)
            ppid.append(post['_id'])
            count = count+1 

            for tag in post['tags']:
                etags.append(tag)
                check_inter = {"_id": 0}
                for inter in interact:
                    # print(inter)
                    if post['_id'] == inter['_id']:
                        inter_f = {"_id": inter['_id'],"interactions" : inter['interactions'],"user_id": 1,"inumber":count,"tags":tag}
                        # print(inter_f)
                        inumber.append(count)
                        iuid.append(1)
                        allinteractions.append(inter_f)
                        check_inter = inter
                        if inter['interactions'] > 1:
                            related.append(inter['_id'])
                        break
                if post['_id'] != check_inter['_id']:
                        blank = {"_id": post['_id'],"interactions" : 0,"user_id": 1,"inumber":count,"tags":tag}
                        # print(blank)
                        inumber.append(count)
                        iuid.append(1)
                        allinteractions.append(blank)
    
    #create interaction all
    convertPost(interact,postdetail)
    # print("x")
    #build dataset
    dataset = Dataset(item_identity_features=False)
    dataset.fit(iuid,inumber)
    dataset.fit_partial(items=tuple(inumber),item_features=etags)
    
    # matrix
    def _get_dimensions(data,users):
        uids = set()
        iids = set()

        for d in data:
            uids.add(users)
            iids.add(d)
        rows = max(uids) + 1
        cols = max(iids) + 1
        return rows, cols

    def _build_interaction_matrix(rows, cols, data, user, min_rating):
        mat = sp.lil_matrix((rows, cols), dtype=np.int32)
        for inter in data:
            mat[user,inter['inumber']] = inter['interactions']
        return mat.tocoo()

    num_users, num_items = _get_dimensions(inumber, useridi)
    # print(num_users)
    # print(num_items)

    interact_matrix = _build_interaction_matrix(num_users, num_items, allinteractions,useridi, min_rating=1)

    # print(interact_matrix)
    item_features = dataset.build_item_features(((x['inumber'], tuple([x['tags']]))
                                              for x in allinteractions),normalize=False)

    # print(item_features)
    # print(dataset.item_features_shape())

    # model
    model = LightFM(loss='warp')
    model.fit(interact_matrix, item_features=item_features)

    #predict
    scores = model.predict(user_ids=useridi, item_ids=inumber, item_features=item_features)
    # print(scores)
    top_items = np.array(list(allinteractions))[np.argsort(-scores)]
    
    recommend =[]
    # print(top_items)
    #choose post to recommend from top item
    counter = 0
    for x in top_items:
        notDirty = True
        # print(x)
        for rec in recommend:
            # print(rec)
            if x['_id']==rec['_id']:
                notDirty = False
                break
        if(notDirty):
            for post in postdetail: 
                # print(post['_id'])
                # print(x['_id'])
                # print("x")
                if counter <10:
                    if x['_id']== post['_id']:
                        print("x")
                        # for r in related:
                        #     print(r)
                            # if r != x['_id']:
                        recommend.append(post)
                        counter = counter + 1
                        # break
                else:
                    break
    print(recommend)
    return recommend
    


