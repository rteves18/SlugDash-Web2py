# These are the controllers for your ajax api.


def get_posts():
    """This controller is used to get the posts.  Follow what we did in lecture 10, to ensure
    that the first time, we get 4 posts max, and each time the "load more" button is pressed,
    we load at most 4 more posts."""
    # Implement me!
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    # We just generate a lot of of data.
    posts = []
    has_more = False
    rows = db().select(db.post.ALL, limitby=(start_idx, end_idx + 1), orderby=~db.post.created_on)
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            # If user is logged in
            if auth.user_id is not None:
                # If current user is user of post
                if r.user_email == get_user_name_from_email(auth.user.email):
                    # If post has been updated
                    if r.created_on != r.updated_on:
                        p = dict(
                            id=r.id,
                            post_content=r.post_content,
                            user_email=r.user_email,
                            created_on=r.created_on,
                            updated_on=r.updated_on,
                            is_author=True,
                            is_updated=True,
                        )
                        # User of post is current user
                        # But post was not updated
                    else:
                        p = dict(
                            id=r.id,
                            post_content=r.post_content,
                            user_email=r.user_email,
                            created_on=r.created_on,
                            updated_on=r.updated_on,
                            is_author=True,
                            is_updated=False,
                        )

                        # User of post is not current user
                        # But post was updated
                else:
                    if r.created_on != r.updated_on:
                        p = dict(
                            id=r.id,
                            post_content=r.post_content,
                            user_email=r.user_email,
                            created_on=r.created_on,
                            updated_on=r.updated_on,
                            is_author=False,
                            is_updated=True,
                        )
                        # User of post is not current user
                        # And post was not updated
                    else:
                        p = dict(
                            id=r.id,
                            post_content=r.post_content,
                            user_email=r.user_email,
                            created_on=r.created_on,
                            updated_on=r.updated_on,
                            is_author=False,
                            is_updated=False,
                        )
            # user is not logged in
            else:
                if auth.user_id is None:
                    p = dict(
                        id=r.id,
                        post_content=r.post_content,
                        user_email=r.user_email,
                        created_on=r.created_on,
                        updated_on=r.updated_on,
                        is_author=False,
                        is_updated=False,
                        )
            posts.append(p)
        else:
            has_more = True
    logged_in = auth.user_id is not None
    return response.json(dict(
        posts=posts,
        logged_in=logged_in,
        has_more=has_more,
    ))

# Note that we need the URL to be signed, as this changes the db.
@auth.requires_signature()
def add_post():
    """Here you get a new post and add it.  Return what you want."""
    # Implement me!
    p_id = db.post.insert(
        post_content=request.vars.post_content,
        user_email = get_user_name_from_email(auth.user.email),
    )
    p = db.post(p_id)
    p.is_author = True
    return response.json(dict(post=p))

"""Edits a post"""
@auth.requires_signature()
def edit_post():
    p = db.post(request.vars.post_id)
    p.update_on = request.vars.edit_date
    p.post_content = request.vars.post_content
    p.updated_on = datetime.datetime.utcnow()
    p.update_record()
    return response.json(dict(post=p, edit_time=datetime.datetime.utcnow()))

@auth.requires_signature()
def del_post():
    """Used to delete a post."""
    # Implement me!
    db(db.post.id == request.vars.post_id).delete()
    return "ok"
    # return response.json(dict())

