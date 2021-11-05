import json
import numpy as np
from lightfm.data import Dataset
from lightfm import LightFM
import scipy.sparse as sp

def lightfmReccomend(interact,postdetail):
    
    # print(interact)
    # print(postdetail)

    # userid = interact[0]['user_id'] # user interact id

    useridi = 1
    ppid = [] # all post ids
    iuid = [] # all user ids (same)
    ipid = [] # 
    tags = [] # all post tags
    inumber = []
    allinteractions = [] # all interactions
    nametags = ("Dogs","Cats","Fishes","Mammals","Insects","Reptiles","Birds","Amphibians",)
    # print(interact)
    def convertPost(interact,postdetail):
        
        count = -1
        for post in postdetail:
            
            # print(post)
            ppid.append(post['_id'])
            ptags = [] # all tags in this post
            count = count+1 
            # print(ptags)
            for tag in post['tags']:
                a = 0
                if tag == "Dogs":
                    a = 1
                elif tag == "Cats":
                    a = 2
                elif tag == "Fishes":
                    a = 3
                elif tag == "Mammals":
                    a = 4
                elif tag == "Insects":
                    a = 5
                elif tag == "Reptiles":
                    a = 6
                elif tag == "Birds":
                    a = 7
                elif tag == "Amphibians":
                    a = 8
                ptags.append(tag)
                # print(ptags)
            
            tags.append(tuple(ptags))

            for inter in interact:
                # print("x")
                if post['_id'] == inter['_id']:
                    inter_f = {"_id": inter['_id'],"interactions" : inter['interactions'],"user_id": 1,"inumber":count,"tags":tuple(ptags)}
                    # print(inter_f['tags'])
                    print(inter_f)
                    inumber.append(count)
                    iuid.append(1)
                    allinteractions.append(inter_f)
                    # allinteractions.append(inter)
                    break
            if post['_id'] != inter_f['_id']:
                    # blank = {"_id": post['_id'],"interactions" : 0,"user_id": userid}
                    blank = {"_id": post['_id'],"interactions" : 0,"user_id": 1,"inumber":count,"tags":tuple(ptags)}
                    print(blank)
                    inumber.append(count)
                    iuid.append(1)
                    allinteractions.append(blank)
        # print(ppid)
        # print(tags)
        # print(allinteractions)

    convertPost(interact,postdetail)

    # def convertInteraction(allinteractions):
    #     for interaction in allinteractions:
    #         iuid.append(interaction["owner"]['user_id'])
    #         ipid.append(interaction['_id'])

    dataset = Dataset(user_identity_features=False)
    dataset.fit(iuid,inumber)
    # num_users, num_items = dataset.interactions_shape()
    # print(num_users)
    # print(num_items)
    print(tags)
    dataset.fit_partial(items=tuple(inumber),item_features=tuple(tags))
    
    # matrix

    def _get_dimensions(data,users):
        uids = set()
        iids = set()
        for d in data:
            uids.add(users)
            iids.add(d)
        # print(uids)
        # print(iids)
        rows = max(uids) + 1
        cols = max(iids) + 1
        return rows, cols

    # def _build_interaction_matrix(rows, cols, data, min_rating):
    #     mat = sp.lil_matrix((rows, cols), dtype=np.int32)
    #     for inter in data:
    #         if inter['interactions'] >= min_rating:
    #             print([inter['user_id'],inter['_id']])
    #             mat[inter['user_id'],inter['_id']] = inter['interactions']
    #     return mat.tocoo()

    # num_users, num_items = _get_dimensions(inumber, useridi)
    # interact_matrix = _build_interaction_matrix(num_users, num_items, allinteractions, min_rating=1)
    # print("x")
    def _build_interaction_matrix(rows, cols, data, user, min_rating):
        mat = sp.lil_matrix((rows, cols), dtype=np.int32)
        for inter in data:
            if inter['interactions'] >= min_rating:
                # print("x")
                # print(user,interidf)
                # print(inter['interactions'])
                # print([inter['user_id'],inter['_id']])
                mat[user,inter['inumber']] = inter['interactions']
        return mat.tocoo()
    # print("x")
    # print(inumber)
    # print(useridi)
    num_users, num_items = _get_dimensions(inumber, useridi)
    # print("x")
    # print(num_users)
    # print(num_items)

    interact_matrix = _build_interaction_matrix(num_users, num_items, allinteractions,useridi, min_rating=1)
    # (interact_matrix, weights) = dataset.build_interactions(((x['user_id'], x['inumber'])
    #                                                             for x in allinteractions))

    # print(interact_matrix)
    # item_features = dataset.build_item_features(tuple((inumber), [tags]))
    # print("x")
    # for x in ((x['inumber'], [x['tags']]) for x in allinteractions):
    #     print(x)
    item_features = dataset.build_item_features(((x['inumber'], [x['tags']])
                                              for x in allinteractions))
    
    print(interact_matrix)

    print(item_features)

    # model
    model = LightFM(loss='bpr')
    model.fit(interact_matrix, item_features=item_features)

    def sample_recommendation(num_users, num_items,data, model, user_id, postdetail):

        scores = model.predict(user_id, np.arange(num_items))
        print(scores)
        top_items = np.array(list(data))[np.argsort(-scores)]
        # print(top_items)
            #print out the results
        # print(user_id)
        # print("     Recommended:")
        result=[]
        for x in top_items[:10]:
            print(x['_id'])
            # print("        %s" % x)
            for post in postdetail:
                # print(post)
                if x['_id']== post['_id']:
                    result.append(post['tags'])
            # result.append(x)
        return result

    recommend = sample_recommendation(num_users, num_items,allinteractions, model, useridi, postdetail)
    return recommend
    # print(recommend)
    # red = (postdetail[x] for x in recommend)
    # # print(recommend)  
    # # print(list(red))
    # return list(red)

    


