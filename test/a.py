from app.api.baidueagle import entity_list

print(entity_list('123')['status']==200)