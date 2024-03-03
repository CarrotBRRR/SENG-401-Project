import { AuthOptions } from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import { authenticateUser, createUser, getUser } from "../actions";

export const authOptions: AuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
    }),
  ],
  callbacks: {
    async session({ session, token }) {
      // WAITING ON BACKEND TO COMPLETE THIS FUNCTIONALITY
      // const userData = await authenticateUser(session);
      // const userData = await getUser(session.user?.email || "");
      // const newSession = { userData, ...session };
      // console.log(newSession);
      // return newSession;
      return session;
    },
  },
};
