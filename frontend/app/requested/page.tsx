import { getLenderItems } from "../actions";
import { ItemsGetListI } from "../interfaces/ListItemI";
import ItemRequests from "./ItemRequests";

export default async function page() {
  const res = await getLenderItems()
  const items: ItemsGetListI[] = res.items || [];
  const filteredItems = items.filter((item: ItemsGetListI) =>{
    if(item.borrowRequests && item.borrowRequests.length > 0){
      return true;
    }
    return false
  })

  return <ItemRequests items={filteredItems} />;
}
