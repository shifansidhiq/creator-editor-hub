from django.shortcuts import render

# Create your views here.
from django.db.models import Max
from .models import user_login

def index(request):
    pd_list = portfolio_details.objects.all()
    context ={'pd_list':pd_list}
    return render(request, './myapp/index.html', context)


def about(request):
    return render(request, './myapp/about.html')


def contact(request):
    return render(request, './myapp/contact.html')

#####################################################################################
######################### ADMIN ##################################################
def admin_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='admin')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/admin_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/admin_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/admin_login.html',context)


def admin_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        return render(request,'./myapp/admin_home.html')


def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='admin')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/admin_changepassword.html', context)

from .models import user_details

def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='user')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            pd_list = portfolio_details.objects.all()
            context = {'uname': request.session['user_name'], 'pd_list': pd_list}
            #send_mail('Login','welcome'+uname,uname)
            return render(request, 'myapp/user_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')
    

def admin_creator_details_view(request):
    tm_l = creator_details.objects.all()
    context = {'creator_list': tm_l, 'msg':'', 'type':'Creator Details'}
    return render(request, './myapp/admin_creator_details_view.html',context)

def admin_user_details_view(request):
    tm_l = user_details.objects.all()
    context = {'user_list': tm_l, 'msg':'', 'type':'User Details'}
    return render(request, './myapp/admin_user_details_view.html',context)



def admin_user_report_view(request):

    user_id = request.session['user_id']

    pm_l = user_report.objects.all()

    ud_l = user_details.objects.all()
    cd_l = creator_details.objects.all()

    context ={'user_list':ud_l,'creator_list':cd_l,'report_list': pm_l,'msg':''}
    return render(request,'myapp/admin_user_report_view.html',context)



def admin_user_report_block(request):
    id = request.GET.get('id')
    house_id = request.GET.get('house_id')
    print("id="+id)
    pp = user_report.objects.get(id=int(id))
    pp.status = 'blocked'
    pp.save()
    cd_obj = creator_details.objects.get(user_id=pp.arch_id)
    cd_obj.status= 'blocked'
    cd_obj.save()
    pm_l = user_report.objects.all()

    ud_l = user_details.objects.all()
    cd_l = creator_details.objects.all()

    context ={'user_list':ud_l,'creator_list':cd_l,'report_list': pm_l,'msg':'Account Blocked'}
    return render(request,'myapp/admin_user_report_view.html',context)

##############################################################################
############## CREATOR ###################################



from .models import creator_details

def creator_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='creator')
        print(len(ul))
        if len(ul) == 1:

            cd_obj = creator_details.objects.get(user_id=ul[0].id)
            if cd_obj.status == 'blocked':
                context = {'msg': 'Account Blocked'}
                return render(request, 'myapp/creator_login.html',context)
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}
            #send_mail('Login','welcome'+uname,uname)
            return render(request, 'myapp/creator_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/creator_login.html',context)
    else:
        return render(request, 'myapp/creator_login.html')

def creator_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/creator_home.html',context)
    #send_mail("heoo", "hai", '@gmail.com')

# 2. creator_details - id, user_id, fname, lname, pic, dob, gender, email, contact, status

from django.core.files.storage import FileSystemStorage
def creator_details_add(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic = fs.save(uploaded_file.name, uploaded_file)

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('pwd')
        uname=email
        status = "new"

        ul = user_login(uname=uname, passwd=password, u_type='creator')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = creator_details(user_id=user_id,fname=fname, lname=lname,  contact=contact, 
                             email=email, status=status, pic=pic, gender=gender, dob=dob )
        ud.save()

        print(user_id)
        context = {'msg': 'Creator Registered'}
        return render(request, 'myapp/creator_login.html',context)

    else:
        return render(request, 'myapp/creator_details_add.html')

def creator_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, passwd=current_password)

            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/creator_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/creator_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/creator_changepassword.html', context)
    else:
        return render(request, './myapp/creator_changepassword.html')



def creator_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return creator_login_check(request)
    else:
        return creator_login_check(request)

# 3. portfolio_details - id, creator_id, title, test_url, descp, pic1, pic2, pic3, dt, tm, price, status
from datetime import datetime

from .models import portfolio_details
def creator_portfolio_details_add(request):
    if request.method == 'POST':

        user_id = int(request.session['user_id'])
        
        fs = FileSystemStorage()
        
        uploaded_file1 = request.FILES['document1']
        pic1 = fs.save(uploaded_file1.name, uploaded_file1)
        
        uploaded_file2 = request.FILES['document2']
        pic2 = fs.save(uploaded_file2.name, uploaded_file2)

        uploaded_file3 = request.FILES['document3']
        pic3 = fs.save(uploaded_file3.name, uploaded_file3)


        uploaded_file4 = request.FILES['document4']
        filepath = fs.save(uploaded_file3.name, uploaded_file4)

        title = request.POST.get('title')
        descp = request.POST.get('descp')
        test_url = request.POST.get('test_url')
        price = request.POST.get('price')
        
        dt = datetime.today().strftime('%Y-%m-%d')
        tm=' '
        status='ok'
        cs_obj = portfolio_details(title=title, descp=descp, test_url=test_url,
                                pic1=pic1,  pic2=pic2, pic3=pic3,filepath=filepath, 
                                price=price, creator_id=user_id, dt=dt,
                                tm=tm, status=status)
        cs_obj.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/creator_portfolio_details_add.html', context)
    else:
        
        context = {}
        return render(request, './myapp/creator_portfolio_details_add.html', context)


def creator_portfolio_details_delete(request):
    user_id = int(request.session['user_id'])
    id = request.GET.get('id')
    print('id = '+id)
    tm = portfolio_details.objects.get(id=int(id))
    tm.delete()
    msg = 'Record Deleted'
    tm_l = portfolio_details.objects.filter(creator_id=user_id)
    context = {'portfolio_list': tm_l, 'msg':msg}
    return render(request, './myapp/creator_portfolio_details_view.html',context)


def creator_portfolio_details_view(request):
    user_id = int(request.session['user_id'])
    msg = ''
    tm_l = portfolio_details.objects.filter(creator_id=user_id)
    context = {'portfolio_list': tm_l, 'msg':msg}
    return render(request, './myapp/creator_portfolio_details_view.html',context)


def creator_transaction_view(request):
    user_id = int(request.session['user_id'])
    pd_list = portfolio_details.objects.filter(creator_id=user_id)
    t_list = []

    for pd in pd_list:
        p_list = purchase_details.objects.filter(portfolio_id=pd.id)
        t_list.extend(p_list)
    
    user_list = user_details.objects.all()
    category_list = portfolio_details.objects.all()

    context = {'t_list': t_list, 'user_list':user_list,
               'category_list': category_list}
    return render(request, './myapp/creator_transaction_view.html', context)

def creator_portfolio_allratings_view(request):
    portfolio_id = request.GET.get('portfolio_id')
    pr_l = portfolio_rating.objects.filter(portfolio_id=portfolio_id)
    umd = user_details.objects.all()
    context = {'review_list': pr_l,'user_list': umd, 'portfolio_id': portfolio_id, 'msg': ''}
    return render(request, 'myapp/creator_portfolio_allratings_view.html', context)



def creator_user_proposal_view(request):

    user_id = request.session['user_id']

    pm_l = user_proposal.objects.filter(arch_id=int(user_id))

    ar_l = user_details.objects.all()
    context ={'user_list':ar_l,'proposal_list': pm_l,'msg':''}
    return render(request,'myapp/creator_user_proposal_view.html',context)


def creator_user_proposal_reply(request):
    if request.method == 'POST':

        u_file = request.FILES['document']
        fs = FileSystemStorage()
        filepath = fs.save(u_file.name, u_file)

        user_id = request.session['user_id']
        proposal_id = int(request.POST.get('proposal_id'))
        remark = request.POST.get('remark')
        amt = request.POST.get('amt')

        suc = user_proposal.objects.get(id=int(proposal_id))
        suc.remark = remark
        suc.filepath=filepath
        suc.amt=amt
        suc.status = 'PAYMENT'
        suc.save()

        pm_l = user_proposal.objects.filter(arch_id=int(user_id))

        ar_l = user_details.objects.all()
        context = {'user_list': ar_l, 'proposal_list': pm_l, 'msg': ''}
        return render(request, 'myapp/creator_user_proposal_view.html', context)

    else:
        user_id = request.session['user_id']
        proposal_id = int(request.GET.get('id'))

        context = { 'proposal_id': proposal_id}
        return render(request, './myapp/creator_user_proposal_reply.html', context)


############################################################################
############################### USER ########################################
def user_home(request):

    pd_list = portfolio_details.objects.all()
    
    context = {'uname':request.session['user_name'],'pd_list':pd_list}
    return render(request,'./myapp/user_home.html',context)
    #send_mail("heoo", "hai", 'snehadavisk@gmail.com')

# 6. user_details - id, user_id, fname, lname, contact, email, status
def user_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('pwd')
        uname=email
        status = "new"

        ul = user_login(uname=uname, passwd=password, u_type='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = user_details(user_id=user_id,fname=fname, lname=lname,  contact=contact, email=email , status=status)
        ud.save()

        print(user_id)
        context = {'msg': 'User Registered'}
        return render(request, 'myapp/user_login.html',context)

    else:
        return render(request, 'myapp/user_details_add.html')

def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, passwd=current_password)

            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/user_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/user_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/user_changepassword.html', context)
    else:
        return render(request, './myapp/user_changepassword.html')



def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)


def user_portfolio_details_view(request):
    # user_id = int(request.session['user_id'])
    msg = ''
    tm_l = portfolio_details.objects.all()
    context = {'portfolio_list': tm_l, 'msg':msg}
    return render(request, './myapp/user_portfolio_details_view.html',context)

# def user_crea_details_view(request):
#     pd_list = portfolio_details.objects.all()
#     context = {'patient_list':pd_list,'type':'Patient Details'}
#     return render(request, './myapp/staff_patient_details_view.html',context)

def user_portfolio_details_search(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        tm_l = portfolio_details.objects.filter(descp__contains=key)
        context = {'portfolio_list': tm_l, 'msg':''}
        return render(request, './myapp/user_portfolio_details_view.html',context)

    else:
        return render(request, 'myapp/user_portfolio_details_search.html')

def user_creator_details_search(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        tm_l = creator_details.objects.filter(fname__contains=key)
        context = {'creator_list': tm_l, 'msg':'', 'type':'Creator Details'}
        return render(request, './myapp/user_creator_details_view.html',context)

    else:
        return render(request, 'myapp/user_creator_details_search.html')


def user_creator_profile_view(request):
    id = request.GET.get('id')
    tm = creator_details.objects.get(id=int(id))
    pd_list = portfolio_details.objects.filter(creator_id=tm.user_id)
    print(len(pd_list))
    context = {'cobj': tm, 'msg':'', 'type':'Creator Details', 'pd_list': pd_list}
    return render(request, './myapp/user_creator_profile_view.html',context)

    

# 4. portfolio_rating - id, user_id, portfolio_id, rating, review, dt, tm, status

from .models import portfolio_rating
def user_portfolio_rating_add(request):
    if request.method == 'POST':
        portfolio_id = request.POST.get('portfolio_id')
        user_id = request.session['user_id']
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'ok'
        pr = portfolio_rating(portfolio_id=int(portfolio_id),user_id=int(user_id),rating=int(rating),review=review,
                            dt=dt,tm=tm)
        pr.save()

        context = {'msg':'Review added','portfolio_id':portfolio_id}
        return render(request, 'myapp/user_portfolio_rating_add.html',context)

    else:
        portfolio_id = request.GET.get('portfolio_id')
        context = {'msg':'','portfolio_id':portfolio_id}
        return render(request, 'myapp/user_portfolio_rating_add.html',context)

# def user_user_ratings_delete(request):
#     id = request.GET.get('id')
#     house_id = request.GET.get('house_id')
#     print("id="+id)
#     pp = user_ratings.objects.get(id=int(id))
#     pp.delete()

#     user_id = request.session['user_id']
#     house_id = request.GET.get('house_id')
#     pr_l = user_ratings.objects.filter(house_id=house_id, user_id=int(user_id))
#     context = {'review_list': pr_l, 'house_id': house_id, 'msg': 'Review deleted'}
#     return render(request, 'myapp/user_user_ratings_delete.html', context)

# def user_user_ratings_view(request):
#     user_id=request.session['user_id']
#     house_id = request.GET.get('house_id')
#     pr_l = user_ratings.objects.filter(house_id=house_id,user_id=int(user_id))
#     context = {'review_list': pr_l, 'house_id': house_id, 'msg': ''}
#     return render(request, 'myapp/user_user_ratings_view.html', context)

def user_portfolio_allratings_view(request):
    portfolio_id = request.GET.get('portfolio_id')
    pr_l = portfolio_rating.objects.filter(portfolio_id=portfolio_id)
    umd = user_details.objects.all()
    context = {'review_list': pr_l,'user_list': umd, 'portfolio_id': portfolio_id, 'msg': ''}
    return render(request, 'myapp/user_portfolio_allratings_view.html', context)


# 5. purchase_details - id, portfolio_id, user_id, dt, tm, amt, payment_type, remarks, status


from .models import purchase_details
import time
def user_payments_add(request):
    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        portfolio_id = int(request.POST.get('portfolio_id'))
        user_id = request.POST.get('user_id')
        payment_type = request.POST.get('mode_of_pay')
        amt = request.POST.get('amt')
        remarks = request.POST.get('card_no')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'closed'
        
        bm_obj = purchase_details(portfolio_id=portfolio_id, user_id=int(user_id), 
                    dt=dt, tm=tm, amt=amt, payment_type=payment_type, remarks=remarks, status=status)
        bm_obj.save()
        
        context = {'msg': f'Payment Success'}

        return render(request, './myapp/user_msg.html', context)
    else:
        portfolio_id = int(request.GET.get('portfolio_id'))
        tbm_obj = portfolio_details.objects.get(id=portfolio_id)
        amt = tbm_obj.price
        user_id=request.session['user_id']
        context = {'portfolio_id':portfolio_id, 'amt':amt, 'user_id':user_id}
        return render(request, './myapp/user_payments_add.html', context)

def user_transaction_view(request):
    user_id = int(request.session['user_id'])
    t_list = purchase_details.objects.filter(user_id=user_id)
    user_list = user_details.objects.all()
    category_list = portfolio_details.objects.all()

    context = {'t_list': t_list, 'user_list':user_list,
               'category_list': category_list}
    return render(request, './myapp/user_transaction_view.html', context)


def user_purchased_portfolio_details_view(request):
    user_id = int(request.session['user_id'])
    msg = ''
    tm_l = []
    pd_list = purchase_details.objects.filter(user_id=user_id)
    for pd in pd_list:
        pd_obj = portfolio_details.objects.get(id=pd.portfolio_id)
        tm_l.append(pd_obj)
    context = {'portfolio_list': tm_l, 'msg':msg}
    return render(request, './myapp/user_portfolio_details_view2.html',context)



from .models import user_proposal

def user_creator_proposal_add(request):
    if request.method == 'POST':
        # u_file = request.FILES['document']
        # fs = FileSystemStorage()
        # filepath = fs.save(u_file.name, u_file)

        requirments = request.POST.get('requirments')
        remark = 'no remarks'
        arch_id = int(request.POST.get('arch_id'))
        user_id = request.session['user_id']
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        pm = user_proposal(user_id=int(user_id),arch_id=arch_id,filepath='no file',
                           requirments=requirments,remark=remark,amt='0',dt=dt,tm=tm,status='PENDING' )
        pm.save()

        context = {'arch_id':arch_id,'msg':'Record added'}
        return render(request, 'myapp/user_creator_details_search.html',context)

    else:
        arch_id = int(request.GET.get('arch_id'))

        context = {'arch_id':arch_id,'msg':''}
        return render(request, 'myapp/user_creator_proposal_add.html',context)

def user_creator_proposal_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    pm = user_proposal.objects.get(id=int(id))
    pm.delete()


    user_id = request.session['user_id']

    pm_l = user_proposal.objects.filter(user_id=int(user_id))

    ar_l = creator_details.objects.all()
    context ={'architect_list':ar_l,'proposal_list': pm_l,'msg':'Record deleted'}
    return render(request,'myapp/user_creator_proposal_view.html',context)

def user_creator_proposal_view(request):

    user_id = request.session['user_id']

    pm_l = user_proposal.objects.filter(user_id=int(user_id))

    ar_l = creator_details.objects.all()
    context ={'architect_list':ar_l,'proposal_list': pm_l,'msg':''}
    return render(request,'myapp/user_creator_proposal_view.html',context)




def user_payments_add2(request):
    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        proposal_id = int(request.POST.get('proposal_id'))
        # user_id = request.POST.get('user_id')
        
        bm_obj = user_proposal.objects.get(id=proposal_id)
        bm_obj.status='PAID'
        bm_obj.save()
        
        context = {'msg': f'Payment Success'}

        return render(request, './myapp/user_msg.html', context)
    else:
        proposal_id = int(request.GET.get('proposal_id'))
        tbm_obj = user_proposal.objects.get(id=proposal_id)
        amt = tbm_obj.amt
        user_id=request.session['user_id']
        context = {'proposal_id':proposal_id, 'amt':amt, 'user_id':user_id}
        return render(request, './myapp/user_payments_add2.html', context)

# def user_creator_proposal_pending_view(request):

#     user_id = request.session['user_id']

#     pm_l = user_proposal.objects.filter(user_id=int(user_id), status='PENDING')

#     ar_l = creator_details.objects.all()
#     context ={'architect_list':ar_l,'proposal_list': pm_l,'msg':''}
#     return render(request,'myapp/user_creator_proposal_view.html',context)


from .models import user_report

def user_report_add(request):
    if request.method == 'POST':

        requirments = request.POST.get('requirments')
        remark = 'no remarks'
        arch_id = int(request.POST.get('arch_id'))
        user_id = request.session['user_id']
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        pm = user_report(user_id=int(user_id),arch_id=arch_id,
                           requirments=requirments,remark=remark,dt=dt,tm=tm,status='PENDING' )
        pm.save()

        context = {'arch_id':arch_id,'msg':'Report Send'}
        return render(request, 'myapp/user_creator_details_search.html',context)

    else:
        arch_id = int(request.GET.get('arch_id'))

        context = {'arch_id':arch_id,'msg':''}
        return render(request, 'myapp/user_report_add.html',context)

# def user_creator_proposal_delete(request):
#     id = request.GET.get('id')
#     print("id="+id)

#     pm = user_proposal.objects.get(id=int(id))
#     pm.delete()


#     user_id = request.session['user_id']

#     pm_l = user_proposal.objects.filter(user_id=int(user_id))

#     ar_l = creator_details.objects.all()
#     context ={'architect_list':ar_l,'proposal_list': pm_l,'msg':'Record deleted'}
#     return render(request,'myapp/user_creator_proposal_view.html',context)

def user_report_view(request):

    user_id = request.session['user_id']

    pm_l = user_report.objects.filter(user_id=int(user_id))

    ar_l = creator_details.objects.all()
    context ={'architect_list':ar_l,'report_list': pm_l,'msg':''}
    return render(request,'myapp/user_report_view.html',context)
