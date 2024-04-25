@ulashuv_router.post("/add")
async def user_add(ulashuv_id: int,
                   video_id: int,
                   follower_id: int,
                   #    files: typing.Optional[list[UploadFile]] = [File(None)],
                   db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)
                   ):
    # new_uservideo = Ulashuv(
    #
    #     user_id=current_user.id,
    #     video_id=video_id,
    #
    # )
    # db.add(new_uservideo)
    # db.commit()

    ulashuv = db.query(Ulashuv).filter_by(id=id).first()

    if not ulashuv:
        print("Ulashuv topilmadi")

    if len(ulashuv.ulash_files) == 0:
        print("Ulashuv fayllari mavjud emas")

    for file in ulashuv.ulash_files:
        if file.number is None:
            file.number = 0
        file.number += 1

    ulashuv.user_id = current_user.id
    ulashuv.video_id = video_id
    ulashuv.follwer_id = follower_id

    db.commit()
