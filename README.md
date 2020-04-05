# Spending Tracker API

This small [Flask](https://palletsprojects.com/p/flask/) application aims to help you **track your expenses**. 

You can clone, configure, and deploy your instance (to [Heroku](https://www.heroku.com/) or elsewhere).
You will be able to track your expenses *with no corporation monitoring your outgoings*.

> You find the related front-end application [here](https://github.com/janos-gonye/spending-tracker-cross-platform-front-end).

### What to use it for:
- Create an arbitrary number of categories and subcategories.
- Add transactions of the expense categories.
- Merge categories.
- List transactions by category.
- Show statistics and export them, which sent automatically to your registered email address.
- Users can register by email address. So your friends, relatives, and loved ones can use it, too.

## Setup for development with `Docker`

0. Install `docker` and `docker-compose` if not installed
1. Clone repository
```bash
git clone https://github.com/janos-gonye/spending-tracker-api.git
cd ./spending-tracker-api
```
2. Create `.env` file and set environment variables. See `.env.template` for help.
```bash
touch .env
```

3. Run docker-compose
```
docker-compose up --build
```
4. Visit http://localhost:5000/.

## API Endpoints

#### Registration
***[POST]** /api/auth/registration*
```json
{
	"username": "<string:username>",
	"password": "<string:password>"
}
```
***[GET]**  /api/auth/registration/confirm*

<hr>

#### Cancel Account
***[DELETE]** /api/auth/registration*

***[GET]** /api/auth/registration/cancel/confirm*

<hr>

#### Login

***[POST]** /api/auth/login*
```json
{
	"username": "<string:required>",
	"password": "<string:required>"
}
```
***[GET]** /api/auth/verify-token*

#### Change Password
***[POST]** /api/auth/change-password*
```json
{
	"old_password": "<string:required>",
	"new_password": "<string:required>"
}
```

#### Forgot Password
***[POST]** /api/auth/forgot-password*
```json
{
	"email": "<string:required>"
}
```

#### Reset Password
***[GET]** /api/auth/reset-password*

<hr>

#### CRUD Categories

***[GET]** /api/categories*

***[POST]** /api/categories*
```json
{
	"title": "<string:required>",
	"description": "<string:optional>",
	"parent_id": "<string|null:optional>"
}
```
***[GET]** /api/categories/<int:category_id>*

***[PATCH]** /api/categeries/<int:category_id>*

```json
{
	"title": "<string:optional>",
	"description": "<string:optional>",
	"parent_id": "<string|null:optional>"
}
```
***[DELETE]** /api/categories/<int:category_id>*

***[POST]** /api/merge-categories*

```json
{
	"subject_id": "<number:required>",
	"target_id":  "<number:required>"
}
```

<hr>

#### CRUD Transactions

***[GET]** /api/categories/<int:category_id  OR "\*">/transactions?from=<number|string:optional>&to=<number|string:optional>*

> *Query parameters 'from', 'to' and key 'processed_at' are UNIX timestamps.*  
> *Query parameters 'from' and 'to' are optional.*

***[POST]** /api/categories/<int:category_id>/transactions*
```json
{
    "amount": "<number:required>",
    "processed_at": "<number|string:required>",
    "comment": "<string:optional>"
}
```
***[GET]** /api/categories/<int:category_id>/transactions/<int:transaction_id>*

***[PATCH]** /api/categories/<int:category_id>/transactions/<int:transaction_id>*
```json
{
    "amount": "<number:optional>",
    "processed_at": "<number|string:optional>",
    "comment": "<string:optional>"
}
```
***[DELETE]** /api/categories/<int:category_id>/transactions/<int:transaction_id>*

<hr>

#### Statistics

***[GET]** /api/statistics*

***[GET]** /api/statistics/export*

<hr>
<br>

*Thanks for reading,*  
*Johnny*
