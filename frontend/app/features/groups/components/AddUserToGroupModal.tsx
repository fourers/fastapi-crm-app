import { useState } from "react";

import type { SearchResult } from "~/features/search/api/types";
import { SearchModal } from "~/features/search/components/SearchModal";
import { searchUsers } from "~/features/users/api/client";

import { useAddGroupUser } from "../api/mutations";

interface AddUserToGroupModalProps {
  groupId: string;
}

export const AddUserToGroupModal = ({ groupId }: AddUserToGroupModalProps) => {
  const [show, setShow] = useState(false);
  const { mutate, isPending } = useAddGroupUser(groupId);
  const [resetKey, setResetKey] = useState(0);

  const addButton = (data: SearchResult) => (
    <div
      className="btn btn-link"
      onClick={() => {
        mutate(
          { userId: data.id },
          {
            onSuccess: () => {
              setShow(false);
              setResetKey((key) => key + 1);
            },
          },
        );
      }}
    >
      Add
    </div>
  );

  return (
    <>
      <div className="btn btn-link" onClick={() => setShow(true)}>
        Add User
      </div>
      <SearchModal
        show={show}
        disabled={isPending}
        onHide={() => setShow(false)}
        searchFunc={searchUsers}
        appendComponent={addButton}
        resetKey={resetKey}
      />
    </>
  );
};
