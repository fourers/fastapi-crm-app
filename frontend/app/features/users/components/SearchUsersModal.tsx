import { useState } from "react";

import { SearchModal } from "~/features/search/components/SearchModal";
import { searchUsers } from "~/features/users/api/client";

export const SearchUsersModal = () => {
  const [show, setShow] = useState(false);

  return (
    <>
      <div className="btn" onClick={() => setShow(true)}>
        Show Search
      </div>
      <SearchModal
        show={show}
        onHide={() => setShow(false)}
        searchFunc={searchUsers}
      />
    </>
  );
};
