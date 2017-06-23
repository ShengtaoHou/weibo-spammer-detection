import csv

attnum=4 #attribute number
attrname=['content_similar','figure_url','figure_jing','follow_ratio','average_repost'] #attribute name
baseline=[13,0.4,0.6,10,5] #baseline that divide attribute number into high part and low part
group_num=10 # group number

precision1=0.0
recall1=0.0
precision2=0.0
recall2=0.0
f1score1=0.0
f1score2=0.0

class att:
    name=''
    high_spam=0
    low_spam=0
    high_nonspam=0
    low_nonspam=0
    baseline=0.0
    num=0.0
    sum=0
    spam_sum=0
    nonspam_sum=0

attlist = [ att() for i in range(attnum)] 
      
for i in range(attnum):
    attlist[i].name=attrname[i]
    attlist[i].baseline=baseline[i]
    

rownum=1
test_group=1

for test_group in range(0,group_num):
    with open(r"spammer.csv","r",encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rownum=rownum+1
            if rownum%group_num!=test_group: 
                for i in range(attnum):                 
                    attlist[i].num=float(row.get(attlist[i].name))
                    is_spam=row.get('is_spammer')
                    if attlist[i].num>=attlist[i].baseline and is_spam=='yes':
                        attlist[i].high_spam=attlist[i].high_spam+1
                    elif attlist[i].num<attlist[i].baseline and is_spam=='yes':
                        attlist[i].low_spam=attlist[i].low_spam+1
                    elif attlist[i].num>=attlist[i].baseline and is_spam=='no':
                        attlist[i].high_nonspam=attlist[i].high_nonspam+1
                    elif attlist[i].num<attlist[i].baseline and is_spam=='no':
                        attlist[i].low_nonspam=attlist[i].low_nonspam+1

    for i in range(attnum):
        attlist[i].sum=attlist[i].high_spam + attlist[i].low_spam + attlist[i].high_nonspam + attlist[i].low_nonspam
        attlist[i].spam_sum=attlist[i].high_spam + attlist[i].low_spam
        attlist[i].nonspam_sum=attlist[i].high_nonspam + attlist[i].low_nonspam 
        
    
    
    spam_p=1.0*attlist[1].spam_sum/(attlist[1].sum)
    nonspam_p=1.0*attlist[1].nonspam_sum/(attlist[1].sum)

    
    tp=0
    tn=0
    fp=0
    fn=0
    rownum=1
    with  open(r"spammer.csv","r",encoding='UTF-8') as csvfile2:
        reader = csv.DictReader(csvfile2) 
        for row in reader:
                rownum=rownum+1
                ps=1.0
                pns=1.0
                if rownum%group_num==test_group:
                    for i in range(attnum):  
                        cur_num=float(row.get(attlist[i].name))
                        is_spam=row.get('is_spammer')
                        if cur_num>=attlist[i].baseline :
                            ps=ps*(1.0*attlist[i].high_spam/attlist[i].spam_sum)
                            pns=pns*(1.0*attlist[i].high_nonspam/attlist[i].nonspam_sum) 
                        elif cur_num<attlist[i].baseline:
                            ps=ps*(1.0*attlist[i].low_spam/attlist[i].spam_sum)
                            pns=pns*(1.0*attlist[i].low_nonspam/attlist[i].nonspam_sum)
                        
                        ps=1.0*ps*spam_p
                        pns=1.0*pns*nonspam_p
                        
                    if ps>pns and is_spam=="yes":
                        tp=tp+1
                    elif ps<pns and is_spam=="no":
                        tn=tn+1
                    elif ps<=pns and is_spam=="yes":
                        fp=fp+1
                    elif ps>=pns and is_spam=="no":
                        fn=fn+1

    precision1=1.0*tp/(tp+fp)+precision1
    precision2=1.0*tn/(tn+fn)+precision2
    recall1=1.0*tp/(tp+fn)+recall1
    recall2=1.0*tn/(tn+fp)+recall2                

precision1=precision1/group_num
precision2=precision2/group_num
recall1=recall1/group_num
recall2=recall2/group_num

f1score1=2.0*precision1*recall1/(precision1+recall1)
f1score2=2.0*precision2*recall2/(precision2+recall2)

print("     precision    recall    f-score")
print("yes  ",round(precision1,2),"        ",round(recall1,2),"     ",round(f1score1,2))
print("no   ",round(precision2,2) ,"        ",round(recall2,2),"     ",round(f1score2,2))
print("avg  ",round((precision1+precision2)/2,2),"        ",round((recall1+recall2)/2,2),"     ",round((f1score1+f1score2)/2,2))