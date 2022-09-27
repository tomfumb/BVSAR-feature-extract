import { useState } from "preact/hooks";

function ModalAuthentication({
  handleAuthenticated = () => {
    console.log("Auth works yay");
  },
}) {
  const [error, setError] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();

    const username = e.target[0].value;
    const password = e.target[1].value;

    const acceptedUsername = import.meta.env.VITE_ACCEPTED_USERNAME;
    const acceptedPassword = import.meta.env.VITE_ACCEPTED_PASSWORD;

    // TODO: Check server health endpoint

    const valid =
      username === acceptedUsername && password === acceptedPassword;

    if (valid) {
      handleAuthenticated();
    } else {
      setError("password");
    }
  }

  const Error = ({ type }) => {
    return (
      <div className="h-44 border-2 border-red-600 p-4 my-2">
        <h3 className="text-lg my-1">Unable to sign in:</h3>
        <p>
          {type === "server"
            ? "Server error"
            : "Incorrect username and password"}
        </p>
      </div>
    );
  };

  const ExplainerBox = () => (
    <div className="my-2 border p-4">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc interdum mi
      sapien, eget tristique augue consequat ac. Proin sed turpis pharetra velit
      scelerisque consequat. Suspendisse aliquam metus a risus fringilla rhoncus
    </div>
  );

  return (
    <div
      className="fixed top-0 w-screen h-screen bg-gray-600/50 flex 
                    justify-center items-center z-10
                   
    "
    >
      <section
        id="authentication"
        className="bg-white shadow-xl 
       w-2/5
      p-4 rounded "
      >
        <h2 className="mb-2 text-2xl">Sign In</h2>
        <form className="flex flex-col" onSubmit={handleSubmit}>
          <label className="text-gray-600 text-sm">username</label>
          <input type="text" className="px-2 py-3 border" />
          <label className="text-gray-600 text-sm">password</label>
          <input type="password" className="px-2 py-3 border" />

          {error ? <Error type={error} /> : <ExplainerBox />}

          <input
            type="submit"
            value="Sign In"
            className="bg-purple-600 text-white p-4 hover:bg-purple-500 cursor-pointer"
          />
        </form>
      </section>
    </div>
  );
}

export default ModalAuthentication;
