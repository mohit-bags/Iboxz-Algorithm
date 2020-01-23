    import numpy as np
    import pandas as pd
    
    candidate_data=[]
    pastExp=3
   
    #data read from a .xlsx file in the system
    data = pd.read_excel('sample_input_job.xlsx')
    corpus=["Technical Expert,Data Analytics, Machine Learning, Financial Services, Human Resources, Legal Services, Engineering, Research, Undergraduate, Associate"]
    #Job Profile Description (#user defined)
    preferable_past_experience = 2 # Default value
    
    #corpus = [corpusString]
    dic1={"Beginner":1,"Intermediate":2,"Advanced":3}

    data["Skill"]=data["Skill"].apply(lambda x : dic1[x])
    
    dic2={"Acquired":1,"Implemented":2}

    data["Skills_Proficiency"]=data["Skills_Proficiency"].apply(lambda x : dic2[x])
    
    #NaNs dropped
    data = data.dropna(axis = 0)
    
    candidate_data = pd.DataFrame({'Name':data['First Name'] +" "+ data['Last Name'],
                                   'Company':data['Company'],
                                   'Job Title':data['Job Title'], 
                                   'Past Experience':data['Past Experience'],
                                   'Skills':(data['Skill']*data['Skills_Proficiency'])  })
                                   
                                 
            
    #Also use endorsements as a scoring parameter, here it's a simulated normal distribution
    #candidate_data['Endorsements'] = np.round(np.random.normal(8, 2, len(candidate_data)), 2)
    #Count Vectorizer imported for NLP
    from sklearn.feature_extraction.text import CountVectorizer

    #Bag of words deployed to create a word dictionary 
    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(corpus)

    #Categories given on the basis of closeness to the job description
    match_score_category = []
    for i in range (0, len(candidate_data)):
        match_array = vectorizer.transform([candidate_data.loc[i, 'Job Title']]).toarray()
        score = 0
        for j in range(0, x.toarray().size):
            if match_array[:, j] == 0:
                score+=0
            else:
                score+=1
        if score>=2:
            match_score_category+= [1]
        elif score == 1 :
            match_score_category+= [2]
        else:
            match_score_category+= [3]
        i+=1
            
        
    candidate_data['Match Score Category jp']= pd.DataFrame({'Match Score Category jp': match_score_category})

    candidate_match_score = []

    for i in range(0, len(candidate_data)):
        if candidate_data.loc[i, 'Match Score Category jp'] == 1:
            candidate_match_score+= [5]
        elif candidate_data.loc[i, 'Match Score Category jp'] == 2:
            candidate_match_score+= [3]
        else:
            candidate_match_score+= [1]
        i+=1
        
    candidate_data['Candidate Match Score jp']= pd.DataFrame({'Candidate Match Score jp': candidate_match_score})

    #Another score parameter on the basis of the past experience of respective candidates    
    candidate_match_score_n = []

    for i in range(0, len(candidate_data)):
        if candidate_data.loc[i, 'Past Experience']>=1 and candidate_data.loc[i, 'Past Experience']<=(preferable_past_experience - 1):
            candidate_match_score_n+=[2]
        elif candidate_data.loc[i, 'Past Experience']>(preferable_past_experience - 1) and candidate_data.loc[i, 'Past Experience']<=(preferable_past_experience + 1):
            candidate_match_score_n+=[3]
        elif candidate_data.loc[i, 'Past Experience']>(preferable_past_experience + 1) and candidate_data.loc[i, 'Past Experience']<=(preferable_past_experience + 3):
            candidate_match_score_n+=[4]
        elif candidate_data.loc[i, 'Past Experience']>(preferable_past_experience + 3):
            candidate_match_score_n+=[5]
        else:
            candidate_match_score_n+=[1]
        i+=1
        
    candidate_data['Candidate Match Score pe']= pd.DataFrame({'Candidate Match Score pe': candidate_match_score_n})
    
    #Another score parameter on the basis of the skills of respective candidates    
    candidate_skill_score=[]
    for i in range(0, len(candidate_data)):
        if candidate_data.loc[i,'Skills']<=2:
            candidate_skill_score+=[1]
        elif candidate_data.loc[i,'Skills']<=4:
            candidate_skill_score+=[2]
        elif candidate_data.loc[i,'Skills']<=6:
            candidate_skill_score+=[3]
        else:
            candidate_skill_score+=[0]
        i+=1
        candidate_data['Candidate Match Score Skills']= pd.DataFrame({'Candidate Match Score Skills': candidate_skill_score})


    
    total_score = []
    for i in range(0, len(candidate_data)):
        total_score+=[(candidate_data.loc[i, 'Candidate Match Score jp'] + 
                       candidate_data.loc[i, 'Candidate Match Score pe'] + 
                       (candidate_data.loc[i, 'Candidate Match Score Skills']*(5/3)))*2/3]
        #+ candidate_data.loc[i, 'Candidate Match Score ed'])*2/3]
        i+=1
        
    candidate_data['Total Score']= pd.DataFrame({'Total Score': total_score})
    
        
    Result = pd.DataFrame({'Name': candidate_data['Name'], 'Match Score': candidate_data['Total Score']})   

    csv = Result.to_csv(encoding='utf-8')

    #return csv


#fileoutput=processData('sample_input.xlsx',5,"Technical Expert, Analytics, Machine Learning, Financial Services, Human Resources, Legal Services, Engineering, Research, Science")
