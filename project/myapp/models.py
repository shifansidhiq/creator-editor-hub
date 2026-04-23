from django.db import models

# 1. user_login - id, uname, passwd, u_type
# 2. creator_details - id, user_id, fname, lname, pic, dob, gender, email, contact, status
# 3. portfolio_details - id, creator_id, title, test_url, descp, pic1, pic2, pic3, dt, tm, price, status
# 4. portfolio_rating - id, user_id, portfolio_id, rating, review, dt, tm, status
# 5. purchase_details - id, portfolio_id, user_id, dt, tm, amt, payment_type, remarks, status
# 6. user_details - id, user_id, fname, lname, contact, email, status
# 7. search_history - id, user_id, keyword, dt, tm, status

# Create your models here.
# 1. user_login - id, uname, passwd, u_type
class user_login(models.Model):
    uname = models.CharField(max_length=100)
    passwd = models.CharField(max_length=25)
    u_type = models.CharField(max_length=10)

    def __str__(self):
        return self.uname

# 2. creator_details - id, user_id, fname, lname, pic, dob, gender, email, contact, status
class creator_details(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    pic = models.CharField(max_length=300)
    dob = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    email = models.CharField(max_length=300)
    contact = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

# 3. portfolio_details - id, creator_id, title, test_url, descp, pic1, pic2, pic3, dt, tm, price, status
class portfolio_details(models.Model):
    creator_id = models.IntegerField()
    title = models.CharField(max_length=100)
    test_url = models.CharField(max_length=100)
    descp = models.CharField(max_length=100)
    pic1 = models.CharField(max_length=100)
    pic2 = models.CharField(max_length=100)
    pic3 = models.CharField(max_length=100) 
    filepath = models.CharField(max_length=300) 
    dt = models.CharField(max_length=100)
    tm = models.CharField(max_length=100)
    price = models.CharField(max_length=100)

    status = models.CharField(max_length=100)

# 4. portfolio_rating - id, user_id, portfolio_id, rating, review, dt, tm, status
class portfolio_rating(models.Model):
    user_id = models.IntegerField()
    portfolio_id = models.IntegerField()
    rating = models.CharField(max_length=100)
    review = models.CharField(max_length=500)
    dt = models.CharField(max_length=100)
    tm = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

# 5. purchase_details - id, portfolio_id, user_id, dt, tm, amt, payment_type, remarks, status
class purchase_details(models.Model):
    portfolio_id = models.IntegerField()
    user_id = models.IntegerField()
    dt = models.CharField(max_length=100)
    tm = models.CharField(max_length=100)
    amt = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=100)
    remarks = models.CharField(max_length=500)
    status = models.CharField(max_length=100)



# 6. user_details - id, user_id, fname, lname, contact, email, status
class user_details(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=250)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.fname

# 7. search_history - id, user_id, keyword, dt, tm, status
class search_history(models.Model):
    user_id = models.IntegerField()
    keyword = models.CharField(max_length=200)
    dt = models.CharField(max_length=100)
    tm = models.CharField(max_length=100)
    status = models.CharField(max_length=100)


class user_proposal(models.Model):
    user_id = models.IntegerField()
    arch_id = models.IntegerField()
    requirments = models.CharField(max_length=250)
    filepath = models.CharField(max_length=250)
    remark = models.CharField(max_length=250)
    amt = models.CharField(max_length=250)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)
    status = models.CharField(max_length=25)


class user_report(models.Model):
    user_id = models.IntegerField()
    arch_id = models.IntegerField()
    requirments = models.CharField(max_length=250)
    remark = models.CharField(max_length=250)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)
    status = models.CharField(max_length=25)
