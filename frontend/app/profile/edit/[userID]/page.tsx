'use client';
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from 'next/navigation'
import { UserI } from "@/app/interfaces/UserI";
import { getUserByID } from "@/app/actions";
import { FaArrowLeft } from "react-icons/fa6";
import { FaRegEdit } from "react-icons/fa";
import { FaCheck } from "react-icons/fa";

export default function Page({ params }: { params: { userID: string } }) {

    const router = useRouter()

    const [name, setName] = useState("");
    const [phone, setPhone] = useState("");
    const [location, setLocation] = useState("");

    const getUserInfo = async () => {
        const res: UserI = await getUserByID(params.userID);
        if (res?.location !== null) {
            setLocation(res?.location)
        }
        if (res?.name !== null) {
            setName(res?.name)
        }
        setPhone(res?.phoneNum || '')
    }

    useEffect(()=> {
        getUserInfo()
    }, [])

    const handleSubmission = async () => {

        var user_name = name
        var user_phone = phone
        var user_location = location
        
        if (name.length === 0) {
            user_name = "none"
        }
        if (phone.length === 0) {
            user_phone = "none"
        }
        if (location.length === 0) {
            user_location = "none"
        }

        console.log("data being sent to db:")
        console.log("name: " + user_name + ", length: " + user_name.length)
        console.log("phone: " + user_phone + ", length: " + user_phone.length)
        console.log("location: " + user_location + ", length: " + user_location.length)
        console.log("end of data")

        // database stuff

        router.push(`/profile/${params.userID}`)
    }

    return (
        <>
            <div className="flex flex-col items-center justify-around w-full">

                <div className="flex flex-row items-center justify-between text-center w-full mb-10">
                    <div className="w-1/3">
                        <Link href={`/profile/${params.userID}`} className="bg-brand rounded-lg hover:cursor-pointer hover:underline w-fit h-fit flex flex-row justify-around items-center text-4xl px-3 py-3">
                            <FaArrowLeft style={{ fontSize: '1em' }}/>
                            <span className="pl-3">Back</span>
                        </Link>
                    </div>
                    <div className="w-1/3 text-4xl text-center font-extrabold">Edit Profile</div>
                    <div className="w-1/3"></div>
                </div>

                <FaRegEdit style={{ fontSize: '7em' }}/>

                <div className="border border-brand mt-20 rounded-lg w-fit h-full flex flex-col justify-center items-center py-5 px-32">
                    <input
                        className="border-2 border-brand bg-white text-black dark:bg-black dark:text-white mt-10 w-full h-16"
                        defaultValue={name}
                        type="text"
                        placeholder='enter name...'
                        onChange={(event) => {
                            setName(event.target.value);
                        }}
                    />
                    <input
                        className="border-2 border-brand bg-white text-black dark:bg-black dark:text-white mt-10 w-full h-16"
                        defaultValue={phone}
                        type="text"
                        placeholder='enter phone number...'
                        onChange={(event) => {
                            setPhone(event.target.value);
                        }}
                    />
                    <input
                        className="border-2 border-brand bg-white text-black dark:bg-black dark:text-white my-10 w-full h-16"
                        defaultValue={location}
                        type="text"
                        placeholder='enter location...'
                        onChange={(event) => {
                            setLocation(event.target.value);
                        }}
                    />
                </div>

                <button className="bg-brand rounded-lg hover:cursor-pointer hover:underline w-fit h-fit flex flex-row justify-around items-center text-4xl px-3 py-3 mt-10" onClick = {() => handleSubmission()}>
                    <span className="pr-3">Submit</span>
                    <FaCheck style={{ fontSize: '1em' }}/>
                </button>

            </div>
        </>
    );

}