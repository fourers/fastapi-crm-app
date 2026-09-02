import { useState } from "react";

import { SearchModal } from "~/features/search/components/SearchModal";
import { searchUsers } from "~/features/users/api/client";

export const SearchUsersModal = () => {
  const [show, setShow] = useState(false);

  return (
    <>
      <div className="btn btn-link" onClick={() => setShow(true)}>
        Add User
      </div>
      <SearchModal
        show={show}
        onHide={() => setShow(false)}
        searchFunc={searchUsers}
      />
    </>
  );
};
