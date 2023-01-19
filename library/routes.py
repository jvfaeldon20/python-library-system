from datetime        import date
from library         import app, db
from flask           import render_template, redirect, url_for, flash, request
from library.models  import BookItem, User, Borrower
from library.forms   import RegisterForm, LoginForm, BorrowBookForm, AddBookForm
from flask_login     import login_user, logout_user, login_required, current_user



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
    


@app.route('/book',methods=['GET','POST'])
@login_required
def book_page():
    borrow_form         = BorrowBookForm()
    if request.method == 'GET':
        items           = BookItem.query.all()
        owned_items     = Borrower.query.filter_by(username=current_user.username, date_returned=None)
        return render_template('book.html', items=items, borrow_form=borrow_form, owned_items=owned_items)

    if request.method == "POST":
        borrowed_item   = request.form.get('borrowed_item')
        # add to borrower
        borrower_to_add = Borrower(book_title     = borrowed_item, 
                                    username      = current_user.username,
                                    email         = current_user.email,
                                    date_borrowed = date.today())
        db.session.add(borrower_to_add)      
        db.session.commit()

        b_item_object   = BookItem.query.filter_by(title=borrowed_item).first()
        if b_item_object:
            # update stocks
            b_item_object.stocks -= 1
            db.session.commit()
            flash(f'Book borrowed successfully! You can now get this book from the Librarian. Thank you!', category='success')
            return redirect(url_for('book_page'))



@app.route('/book/new',methods=['GET','POST'])
@login_required
def new_book_page():
    book_add_form = AddBookForm()
    if book_add_form.validate_on_submit():
        book_to_add   = BookItem(title       = book_add_form.title.data, 
                                description  = book_add_form.description.data,
                                genre        = book_add_form.genre.data,
                                author       = book_add_form.author.data,
                                stocks       = book_add_form.stocks.data)

        db.session.add(book_to_add)      
        db.session.commit()
        flash(f'Book created successfully. Thank you!', category='success')
        return redirect(url_for('book_page'))
    return render_template('book_add.html',book_add_form=book_add_form)
        


@app.route('/book/del/<int:book_id>',methods=['GET','POST'])
@login_required
def delete_book(book_id):
    if request.method == "POST":
        to_delete_book = BookItem.query.get_or_404(book_id)
        db.session.delete(to_delete_book)
        db.session.commit()
        flash(f'Book deleted successfully. Thank you!', category='success')
        return redirect(url_for('book_page'))
    return render_template('books.html') 



@app.route('/borrower/list')
def borrower_page():
    borrowers        = Borrower.query.filter_by(date_returned=None)
    availables       = BookItem.query.all()
    stocks_borrowed  = Borrower.query.filter_by(date_returned=None).count()
    stocks_available = sum([available.stocks for available in availables])
    return render_template('borrower.html',borrowers=borrowers, stocks_available=stocks_available, stocks_borrowed=stocks_borrowed)



@app.route('/borrower/update/<int:borrower_id>', methods=['GET','POST'])
def borrower_update(borrower_id):
    borrowers            = Borrower.query.filter_by(date_returned=None)
    stocks_available     = BookItem.query.count()
    stocks_borrowed      = Borrower.query.count()
    if request.method == "POST":
        update_borrower  = Borrower.query.filter_by(id=borrower_id).first()
        update_borrower.date_returned = date.today()
        db.session.commit()

        book_item        = BookItem.query.filter_by(title=update_borrower.book_title).first()
        book_item.stocks += 1
        db.session.commit()
        book_stock       = BookItem.query.filter_by(title=update_borrower.book_title).first()
        
        flash(f'Book updated successfully! Your total stocks for this book is now { book_stock.stocks }. Thank you!', category='success')
        return redirect(url_for('borrower_page'))
    return render_template('borrower.html',borrowers=borrowers, stocks_available=stocks_available, stocks_borrowed=stocks_borrowed)



@app.route('/user/list')
def user_page():
    users = User.query.all()
    return render_template('user.html', users=users)



@app.route('/user/register', methods = ['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                              email    = form.email.data,
                              password = form.password1.data,
                              type     = 'loc-1')

        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successsfully! You are now logged in as: { user_to_create.username }', category='success')
        return redirect(url_for('book_page'))
    if form.errors != {}: #if there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the user: {err_msg}', category='danger')
    return render_template('register.html', form=form)



@app.route('/user/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password = form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: { attempted_user.username }', category='success')
            return redirect(url_for('book_page'))
        else:
            flash(f'Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/user/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))



@app.route('/user/search', methods = ['GET','POST'])
def search_user():
    if request.method == 'GET':
        keys = request.args.get("key")
        if keys:
            users = User.query.filter(User.username.like(keys + '%')).all()
        else:
            users = User.query.all()
    return render_template('user.html', users=users)



@app.route('/borrower/search', methods = ['GET','POST'])
def search_borrower():
    if request.method == 'GET':
        keys = request.args.get("key")
        if keys:
            borrowers = Borrower.query.filter(Borrower.book_title.like('%' + keys + '%'),Borrower.email.like('%' + keys + '%')).all()
        else:
            borrowers = Borrower.query.filter_by(date_returned=None)
    return render_template('borrower.html', borrowers=borrowers)



@app.route('/book/search', methods = ['GET','POST'])
def search_book():
    borrow_form         = BorrowBookForm()
    if request.method == 'GET':
        keys = request.args.get("key")
        if keys:
            items         = BookItem.query.filter(BookItem.title.like('%' + keys + '%')|BookItem.genre.like('%' + keys + '%')|BookItem.author.like('%' + keys + '%')).all()
            owned_items   = Borrower.query.filter_by(username=current_user.username, date_returned=None)
        else:
            items         = BookItem.query.all()
            owned_items   = Borrower.query.filter_by(username=current_user.username, date_returned=None)
    return render_template('book.html', items=items,borrow_form=borrow_form,owned_items=owned_items)