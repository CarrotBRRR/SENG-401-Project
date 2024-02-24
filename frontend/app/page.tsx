import { getServerSession } from "next-auth/next";
import { authOptions } from "./utils/authOptions";

export default async function Home() {
  const session = await getServerSession(authOptions);
  return (
    <main>
      <pre>{JSON.stringify(session, null, 2)}</pre>
      main page{" "}
    </main>
  );
}
