import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:tickets/screens/ticket_view.dart';
import 'package:tickets/utils/app_info_list.dart';

import '../utils/app_layout.dart';
import '../utils/app_styles.dart';
import '../widgets/column_layout.dart';
import '../widgets/ticket_tabs.dart';

class TicketScreen extends StatelessWidget {
  const TicketScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = AppLayout.getSize(context);
    return Scaffold(
      backgroundColor: Styles.bgColor,
      body: Stack(
        children: [
          ListView(
            padding: EdgeInsets.symmetric(horizontal: AppLayout.getHeight(20), vertical: AppLayout.getHeight(20)),
            children: [
              Gap(AppLayout.getHeight(40)),
              Text("Tickets", style: Styles.headLineStyle),
              Gap(AppLayout.getHeight(20)),
              const AppTicketTabs(firstTab: "Upcoming", secondTab: "Previous"),
              Gap(AppLayout.getHeight(20)),
              Container(
                padding: EdgeInsets.only(left: AppLayout.getHeight(15)),
                child: TicketView(ticket: ticketList[0], isColor: true),
              ),
              Container(
                padding: EdgeInsets.symmetric(horizontal: 15),
                margin: EdgeInsets.symmetric(horizontal: 15),
                color: Colors.white,
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        AppColumnLayout(firstText: "Flutter DB", secondText: "Passenger", alignment: CrossAxisAlignment.start),

                        AppColumnLayout(firstText: "5221 64565", secondText: "passport", alignment: CrossAxisAlignment.end,),
                      ],
                    )
                  ],
                ),
              )
            ],
          ),
      ],
      ),
    );
  }
}
